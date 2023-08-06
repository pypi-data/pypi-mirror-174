# encoding: utf-8
# api: pep517
# title: flit backend
# description: wraps flit_core.buildapi
# version: 0.3
# depends: python:flit (>=3.0, <4.0)
# license: BSD-3-Clause
# priority: extra
# permissive: 0.1
# pylint: disable=unused-import, wrong-import-position, wrong-import-order
#
# As alternative to pluginconf.setup, this module is using flit as
# pep517 build backend. But adding automagic field lookup of course.
#
# Injecting attributes between ini reading and parameter collection
# turned out easier than expanding on flit_core.buildapi functions.
# And lastly, this just chains to flit.main() to handle collect and
# build tasks.
#
# Dynamic handling currently violates all the package tool requirements:
# <https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dynamic>
# But it does have some interesting side effects.
#  * mixes the override text and file inclusion
#    license = { file = "LICENSE" }
#  * for setuptools compat a long dynamic field is required (but flit hates it)
#    dynamic = ["version", "description", "readme", "requires-python",
#              "license", "keywords", "classifiers", "urls", "entry-points"]
# Not sure yet if the pyproject.toml specs allow for reconcilation here.
# <https://github.com/pypa/flit/issues/605>

"""
monkeypatches flit to use pluginconf sources for packaging with a
`pyproject.toml` like:

<table>
<tr><th>pyproject.toml</th>
    <th>foobar/__init__.py</th></tr>
<tr><td><code><pre>
[build-system]
requires = ["pluginconf", "flit"]
build-backend = "pluginconf.flit"

[project]
name = "foobar"
dynamic = ["*"]
</pre></code></td>
<td><code><pre>
# title: foobar
# description: package summary
# version: 2.5.0
# depends: python:requests >= 2.25
# license: MITL
# classifiers: backend, text
# url: http;//example.org
</pre></code></td></tr>
</table>

Can be invoked per `flit-pluginconf build` or `python -m build`.

<img src="/pluginspec/doc/tip/html/flit.gif" alt="flit - can't believe it's not setup.py!!">
"""


import sys
import os
import re
import functools

import flit_core.common
import flit_core.config

import pluginconf
import pluginconf.setup as psetup



#-- patchy patch
def inject(where):
    """ monkeypatch into module """
    def wrapped(func):
        setattr(where, func.__name__, func)
        wrapped.__doc__ = func.__doc__
        return func
    return wrapped

# patch_flit_config
@inject(flit_core.config)
def read_flit_config(path):
    """ @inject patch_flit_config() with forced dynamic fields """
    ini = flit_core.config.tomli.loads(path.read_text('utf-8'))

    # make fields dynamic (exactly the fields flit allows)
    ini["project"]["dynamic"] = ["version", "description"]
    # maybe also record orig list to omit from pmd_meta update? (in addition to ini.MD.get check)
    for dyn in ['description', 'version']:
        if dyn in ini["project"]:
            del ini["project"][dyn]
        if not dyn in ini["project"]["dynamic"]:
            ini["project"]["dynamic"].append(dyn)

    # turn it into LoadedConfig
    return flit_core.config.prep_toml_config(ini, path)

# patch_metadata
@inject(flit_core.common)
def make_metadata(module, ini_info):
    """ @inject different sourcing order to apply plugin meta fields """
    meta = {
        "name": module.name,
        "provides": [module.name]
    }
    meta.update(ini_info.metadata)
    meta.update(
        pmd_update(
            pluginconf.plugin_meta(filename=module.file),
            ini_info
        )
    )
    if not meta.get("version"):
        meta.update(
            flit_core.common.get_info_from_module(module.file, ['version'])
        )
    #print(meta)
    return flit_core.common.Metadata(meta)

# map plugin meta to flit Metadata
def pmd_update(pmd, ini):
    """ enjoin PMD fields with flit.common.MetaData """
    pmd = psetup.MetaUtils(pmd)
    meta = {
        "summary": pmd.description,
        "version": pmd.version,
        "home_page": pmd.url,
        "author": pmd.author,  # should split this into mail and name
        "author_email": None,
        "maintainer": None,
        "maintainer_email": None,
        "license": pmd.license,  # {name=…}
        "keywords": pmd.get_keywords(),
        "download_url": None,
        "requires_python": pmd.python_requires(),
        "platform": [],
        "supported_platform": pmd.architecture,
        "classifiers": list(pmd.classifiers()) + pmd.trove_license() + pmd.trove_status(),
        "provides": [],
        "requires": [], # supposed to override requires_dist if present
        "obsoletes": [],
        "project_urls": [f"{k}, {v}" for k, v in pmd.project_urls().items()],
        "provides_dist": [],
        "requires_dist": pmd.install_requires() or [],
        "obsoletes_dist": [],
        "requires_external": [],
        "provides_extra": [],
    }
    #print(meta)

    # comment/readme
    for docs in pmd.plugin_doc(), psetup.get_readme():
        if docs["long_description"]:
            meta.update({  # with "long_" prefix cut off
                key[5:]: value for key, value in docs.items()
            })

    # entry_points are in ini file
    for section, entries in pmd.entry_points().items():
        ini.entrypoints[section] = ini.entrypoints.get(section, {})
        for script in entries:
            ini.entrypoints[section].update(
                dict(re.findall("(.+)=(.+)", script))
            )
    #print(ini.entrypoints)
    #print(dir(ini))
    #print((ini.metadata))

    # strip empty entries
    return {
        key: value for key, value in meta.items()
        if value and not ini.metadata.get(key) #?
    }



#-- buildapi
from flit_core.buildapi import (     # These have to be late imports; else they'll
    get_requires_for_build_wheel,    # bind with the original buildapi functions.
    get_requires_for_build_sdist,
    get_requires_for_build_editable,
    prepare_metadata_for_build_wheel,
    prepare_metadata_for_build_editable,
    build_wheel,
    build_editable,
    build_sdist,
)
import flit_core.buildapi  # also permit backend="pluginconf.flit:buildapi"

del inject  # omit from docs

#-- invocation point
from flit import main

if __name__ == "__main__":
    # os.environ["FLIT_ALLOW_INVALID"] = 1  # alternative to patch_flit_config?
    main(sys.argv)
