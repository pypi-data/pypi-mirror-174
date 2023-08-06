# encoding: utf-8
# api: pluginconf
##type: class
# category: config
# title: Dependency verification
# description: Check depends: lines
# depends: pluginconf >= 0.7
# version: 0.5
# state: beta
# license: PD
# priority: optional
# permissive: 0.8
#
# This is a rather basic depends: checker, mostly for local and
# installable modules. It's largely built around streamtuner2
# requirements, and should be customized.
#
# Check().depends()/.valid()
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#  Probes a new plugins` depends: list against installed base modules.
#  Utilizes each version: fields and allows for virtual modules, or
#  alternatives and honors alias: names.
#

""" Dependency validation and consistency checker for updates """


import sys
import re
#import zipfile
import logging
import pluginconf
try:
    from distutils.spawn import find_executable
except ImportError:
    try:
        from compat2and3 import find_executable
    except ImportError:
        find_executable = lambda name: False


# Minimal depends: probing
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
class Check():
    """
    Now this definitely requires customization. Each plugin can carry
    a list of (soft-) dependency names.

    … # depends: config, appcore >= 2.0, bin:wkhtmltoimage, python < 3.5

    Here only in-application modules are honored, system references
    ignored. Unknown plugin names are also skipped. A real install
    helper might want to auto-tick them on, etc. This example is just
    meant for probing downloadable plugins.

    The .valid() helper only asserts the api: string, or skips existing
    modules, and if they're more recent.
    While .depends() compares minimum versions against existing modules.

    In practice there's little need for full-blown dependency resolving
    for application-level modules.

    | Attributes | | |
    |------------|---------|-----------------------------------------------------|
    | api        | list    | allowed api: identifiers for .valid() stream checks |
    | system_deps| bool    | check `bin:app` or `python:package` dependencies    |
    | log        | logging | warning handler                                     |
    | have       | dict    | accumulated list of existing/virtual plugins        |
    """

    # supported APIs
    api = ["python", "streamtuner2"]

    # debugging
    log = logging.getLogger("pluginconf.dependency")

    # ignore bin:… or python:… package in depends
    system_deps = False

    def __init__(self, add=None, core=["st2", "uikit", "config", "action"]):
        """
        Prepare list of known plugins and versions in self.have={}

        | Parameters | | |
        |------------|---------|------------------------------------------------------|
        | add        | dict    | name→pmd of existing/core plugins (incl ver or deps) |
        | core       | list    | name list of virtual plugins                         |
        """
        self.have = {
            "python": {"version": sys.version}
        }

        # inject virtual modules
        for name, meta in (add or {}).items():
            if isinstance(meta, bool):
                meta = 1 if meta else -1
            if isinstance(meta, tuple):
                meta = ".".join(str(n) for n in meta)
            if isinstance(meta, (int, float, str)):
                meta = {"version": str(meta)}
            self.have[name] = meta

        # read plugins/*
        self.have.update(pluginconf.all_plugin_meta())

        # add core modules
        for name in core:
            self.have[name] = pluginconf.plugin_meta(module=name, extra_base=["config"])

        # aliases
        for name, meta in self.have.copy().items():
            if meta.get("alias"):
                for alias in re.split(r"\s*[,;]\s*", meta["alias"]):
                    self.have[alias] = self.have[name]

    def valid(self, new_plugin):
        """
        Plugin pre-screening from online repository stream.
        Fields are $name, $file, $dist, api, id, depends, etc
        Exclude installed or for newer-version presence.

        | Parameters  | | |
        |-------------|---------|------------------------------------------------------|
        | new_plugin  | dict    | online properties of available plugin                |
        | **Returns** | bool    | is updatatable                                       |
        """
        if not "$name" in new_plugin:
            self.log.warning(".valid() checks online plugin lists, requires $name")
        name = new_plugin.get("$name", "__invalid")
        have_ver = self.have.get(name, {}).get("version", "0")
        if name.find("__") == 0:
            self.log.debug("wrong/no id")
        elif new_plugin.get("api") not in self.api:
            self.log.debug("not in allowed APIs")
        elif {new_plugin.get("status"), new_plugin.get("priority")} & {"obsolete", "broken"}:
            self.log.debug("wrong status (obsolete/broken)")
        elif have_ver >= new_plugin.get("version", "0.0"):
            self.log.debug("newer version already installed")
        else:
            return True
        return False

    def depends(self, plugin):
        """
        Verify depends: and breaks: against existing plugins/modules

        | Parameters  | | |
        |-------------|---------|------------------------------------------------------|
        | plugin      | dict    | plugin meta properties of (new?) plugin              |
        | **Returns** | bool    | matches up with existing .have{} installation        |
        """
        result = True
        if plugin.get("depends"):
            result &= self.and_or(self.split(plugin["depends"]), self.have)
        if plugin.get("breaks"):
            result &= self.neither(self.split(plugin["breaks"]), self.have)
        self.log.debug("plugin '%s' matching requirements: %i", plugin["id"], result)
        return result

    def split(self, dep_str):
        """
        Split trivial "pkg | alt, mod>=1, uikit<4.0" string
        into nested list [ [alt, alt], [dep], [dep] ];
        with each entry comprised of (name, operator, version).
        """
        dep_cmp = []
        for alt_str in re.split(r"\s*[,;]+\s*", dep_str):
            alt_cmp = []
            # split alternatives |
            for part in re.split(r"\s*\|+\s*", alt_str):
                # skip deb:pkg-name, rpm:name, bin:name etc.
                if not part:
                    continue
                if part.find(":") >= 0:
                    self.have[part] = {"version": self.module_test(*part.split(":"))}
                # find comparison and version num
                part += " >= 0"
                match = re.search(r"([\w.:-]+)\s*\(?\s*([>=<!~]+)\s*([\d.]+([-~.]\w+)*)", part)
                if match and match.group(2):
                    alt_cmp.append([match.group(i) for i in (1, 2, 3)])
            if alt_cmp:
                dep_cmp.append(alt_cmp)
        return dep_cmp

    def cmp(self, name_op_ver, have, absent=True):
        """ Single comparison """
        name, operator, ver = name_op_ver
        # absent=True is the relaxed check, will ignore unknown plugins
        # set absent=False or None for strict check (as in breaks: rule e.g.)
        if not have.get(name, {}).get("version"):
            return absent
        # curr = installed version
        curr = have[name]["version"]
        tbl = {
            ">=": curr >= ver,
            "<=": curr <= ver,
            "==": curr == ver,
            ">":  curr > ver,
            "<":  curr < ver,
            "!=": curr != ver,
        }
        result = tbl.get(operator, True)
        self.log.debug("VERSION_COMPARE: %s → (%s %s %s) == %s", name, curr, operator, ver, result)
        return result

    def and_or(self, deps, have, inner_true=True):
        """ Compare nested structure of [[dep],[alt,alt]] """
        #print deps
        return not False in [
            inner_true in [self.cmp(d, have) for d in alternatives] for alternatives in deps
        ]

    def neither(self, deps, have):
        """ Breaks/Conflicts: check [[or],[or]] """
        return not True in [
            self.cmp(d, have, absent=None) for cnd in deps for d in cnd
        ]

    def module_test(self, urn, name):
        """ Probes "bin:name" or "python:name" dependency URNs """
        if not self.system_deps:
            return "1"
        if "_" + urn in dir(self):
            if bool(getattr(self, "_" + urn)(name)):
                return "1"
        return "-1" # basically a negative version -v1

    @staticmethod
    def _bin(name):
        """ `bin:name` lookup """
        return find_executable(name)

    @staticmethod
    def _python(name):
        """ `python:module` test """
        return __import__("imp").find_module(name) is not None
