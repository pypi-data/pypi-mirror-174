# encoding: utf-8
# api: pluginconf
##type: loader
# title: plugin loader
# description: implements a trivial unified namespace importer
# version: 0.1
# state: alpha
# priority: optional
#
# Most basic plugin management/loader. It unifies meta data retrieval
# and instantiation. It still doesn't dictate a plugin API or config
# storage (using json in examples). And can be a simpler setup:
#
# Create an empty plugins/__init__.py to use as package and for
# plugin discovery.
#
# Designate it as such:
#
#      import pluginconf.bind  # (first import resets .plugin_base)
#      pluginconf.bind.base("plugins")
#
# Set up a default conf={} in your application, with some presets,
# or updating it from a stored config file:
#
#      conf = {
#          "first_run": 1,
#          "debug": 0,
#          "plugins": {},
#      }
#      conf.update(
#          json.load(open("app.json", "r"))
#      )
#
# Then update defaults from plugins:
#
#      if conf["first_run"]:
#          pluginconf.bind.defaults(conf)
#
# Instantiate plugin modules based on load conf[plugins] state:
#
#      for module in pluginconf.bind.load_enabled(conf):
#          module.register(main_window)
#
# Electing a simple init function often suffices, if plugins don't
# register themselves. Alternatively use a class name aligned with
# the plugin basename to disover it, or dir(), or similar such.
# (This is what "pluginconf imposes no API" means: you still have
# to decide on a convention.)
#
# If you want users to update settings or plugin states, use the
# .window module:
#
#      pluginconf.gui.window(conf, conf["plugins"], files=["plugins/*.py"])
#      json.dump(conf, open("app.json", "w"))
#
# Alternatively there's load() for well-known plugin names, or find()
# to uncover them based on descriptors. Or isolated() to instantiate
# from a different set.
#
# Notably the whole effort makes most sense if you have user-supplied
# plugins and some repository to fetch/update new ones from. (Optional
# meta descriptions are quite suitable to signify beta or experimental
# extensions). If so, entangle the alternative directory to be scanned:
#
#      pluginconf.bind.base("plugins", dir="~/.config/app/usrplugs/")
#      pluginconf.bind.defaults(conf)  # update
#
# A simpler user plugin mechanism might just download a zip:
#
#      usr_pyz = f"{os.environ['HOME']}/.config/app/community.pyz"
#      with open(usr_pyz, "w") as write:
#          write.write(
#              requests.get("http://example.org/usr-plugins.zip").content
#          )
#
# And register that as pyz instead (on startup):
#
#      if os.path.exists(usr_pyz):
#          pluginconf.bind.base("plugins", dir=usr_pyz)
#
# With PySimpleGUI, `conf` could be a psg.UserSettings("app.json") for
# automatic settings+update storage, btw.
#

#-- bit briefer for API docs --
"""
Basic plugin loader implementation for flat namespaces. Ties together
pluginconf lookups and config management for plugin loading in apps.
It's rather basic, and subject to change. Does impose a config dict
format, but no storage still.

### Usage example

    # designate a plugins/*.py package as plugin_base
    import plugins
    import pluginconf.bind
    pluginconf.bind.base(plugins)

    # preset core app settings / load from json, add plugin options
    conf = {
        "plugins": {
        }
    }
    pluginconf.bind.defaults(conf)

    # load conf-enabled plugins, and register modules somehow
    for mod in pluginconf.bind.load_enabled(conf):
        mod.init()

### Find by type

    for name, pmd in pluginconf.bind.find(type="effect").items():
        mod = pluginconf.bind.load(name)
        if pmd.category == "menu":
            main_win.add_menu(mod.menu)

Note that this uses meta data extraction, so should best be confined
for app setup/initialization, not used recurringly. The config state
usage is the preferred method. (Only requires property loading
once, for installation or with `pluginconf.gui.window()` usage.)

----
Method interactions: 🚐 = import, 🧩 = meta, 🧾 = config, 🛠  = setup
"""

import os
import sys
import importlib
import functools
import pluginconf

#-- reset pluginconf if .bind is used
pluginconf.plugin_base = []


def load(name):
    """
    Import individual plugin from any of the base paths 🚐
    (The whole namespace is assumed to be flat, and identifiers to be unique.)

    | Parameters  | | |
    |-------------|--------|-------------------------------|
    | name        | str    | Plugin name in any of the registered plugin_base´s. |
    | **Returns** | module | Imported module               |
    """

    for package in pluginconf.plugin_base:
        if package in ("", "."):
            continue
        module_name = package + "." + name
        if module_name in sys.modules:
            return sys.modules[module_name]
        try:
            return importlib.import_module(module_name)
        except ImportError:
            pass


def base(module, path=None):
    """
    Register module as package/plugin_base. Or expand its search path 🛠 .

    | Parameters  | | |
    |-------------|------------|-------------------------------|
    | module      | module/str | Package basename to later load plugins from |
    | path        | str        | Bind directory or pyz/zip bundle to plugin_base. |
    | **Returns** | None   | -                             |

    Module should be a package, as in a directory and init `plugins/__init__.py`.
    Ideally this module was already imported in main. But parameter may be a string.

    This could be invoked multiple times for the package name to append further
    path= arguments (=./contrib/, =/usr/share/app/extenstions/, or a .pyz). Which
    is functionally identical to delcaring `__path__` in the `package/__init__.py`.
    """

    # if supplied as string, instead of active module
    if isinstance(module, str):
        module = sys.modules.get(module) or __import__(module)

    # add to search list
    if module.__name__ not in pluginconf.plugin_base:
        pluginconf.plugin_base.append(module.__name__)

    # enjoin dir or pyz
    if not hasattr(module, "__path__"):
        module.__path__ = [_dirname(module.__file__)]
    if path:
        module.__path__.append(_dirname(path))


def find(**kwargs):
    """
    Find plugins by any combination of e.g. type= or category= 🧩

    | Parameters  | | |
    |-------------|-----------|-------------------------------------------|
    | type        | str       | Search by type: in plugins                |
    | api         | str       | Matching api: designator                  |
    | category    | str       | Or a menu/category or other attributes    |
    | **Returns** | dict      | basename → `PluginMeta` dict of matches   |
    """

    def has_all(pmd):
        for key, dep in kwargs.items():
            if not pmd.get(key) == dep:
                break
        else:
            return True

    return pluginconf.PluginMeta({
        name: pmd for name, pmd in pluginconf.all_plugin_meta().items() if has_all(pmd)
    })


def load_enabled(conf):
    """
    Import modules that are enabled in conf[plugins]={name:True,…} 🧾 🚐

    | Parameters  | | |
    |-------------|-----------|-------------------------------------------|
    | conf        | dict      | Should contain conf["plugins"] activation states |
    | **Returns** | generator | Of loaded modules                         |
    """
    for name, state in conf.get("plugins", conf).items():
        if not state:
            continue
        if name.startswith("_"):
            continue
        yield load(name)


def defaults(conf):
    """
    Traverse installed plugins and expand config dict with presets 🧩 🧾

    | Parameters  | | |
    |-------------|-----------|-------------------------------------------|
    | conf        | dict 🔁   | Expands the conf dict with preset values from any plugins. |
    | **Returns** | None      | -                                         |
    """
    for name, pmd in pluginconf.all_plugin_meta().items():
        pluginconf.add_plugin_defaults(conf, conf["plugins"], pmd, name)


# pylint: disable=invalid-name
class isolated():
    """
    Context manager for isolated plugin structures.  🛠
    This is a shallow alternative to pluginbase and library-level plugins.
    Temporarily swaps global settings, thus maps most static functions.

        with pluginconf.bind.isolated("libplugins") as bound:
            bound.modules2.init()
            print(
                bound.find(api="library")
            )
    """
    def __init__(self, package):
        self.package = package if isinstance(package, str) else package.__name__
        self.reset = []
        #mod = sys.modules.get(self.package) or __import__(self.package)  # must be a real package
        #if not hasattr(mod, "__path__"):
        #    mod.__path__ = [_dirname(mod.__file__)]

    def __enter__(self):
        """ just swap out global config """
        self.reset, pluginconf.plugin_base = pluginconf.plugin_base, []
        base(self.package)
        return self

    def __exit__(self, *exc):
        pluginconf.plugin_base = self.reset

    @staticmethod
    def load(name):
        """ load module from wrapped package 🚐 """
        return load(name)

    def __getattr__(self, name):
        return self.load(name)

    def get_data(self, *args, **kwargs):
        """ get file relative to encapsulated plugins 🚐 """
        pluginconf.get_data(*args, **kwargs, file_root=self.package)

    @staticmethod
    def find(**kwargs):
        """ find by meta attributes 🧩 """
        return find(**kwargs)

    @staticmethod
    def defaults():
        """ *return* defaults for isolated plugin structure 🧩 🧾 """
        conf = {"plugins": {}}
        defaults(conf)
        return conf


def _enable_cache(state=True):
    """
    Reduce plugin_meta() lookup costs, suitable for repeat find() calls
    """
    if hasattr(pluginconf.plugin_meta, "__wrapped__"):
        if state:
            return
        pluginconf.plugin_meta = pluginconf.plugin_meta.__wrapped__
    elif state:
        decorator = functools.lru_cache(maxsize=None)
        pluginconf.plugin_meta = decorator(pluginconf.plugin_meta)


def _dirname(file):
    """ absolute dirname for file """
    return os.path.dirname(os.path.realpath(file))
