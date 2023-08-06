# encoding: UTF-8
# api: python
##type: gui
# category: io
# title: Config GUI
# description: Display plugins + options in setup window
# version: 0.8
# depends: python:pysimplegui (>= 4.0)
# priority: optional
# config: -
# permissive: 0.5
# pylint: disable=line-too-long
#
# Creates a PySimpleGUI options list. Scans a given list of *.py files
# for meta data, then populates a config{} dict and (optionally) a state
# map for plugins themselves.
#
#    jsoncfg = {}
#    pluginconf.gui.window(jsoncfg, {}, ["plugins/*.py"])
#
# Very crude, and not as many widgets as the Gtk/St2 implementation.
# Supports type: str, bool, select, int, dict, text config: options.
#

"""
PySimpleGUI window to populate config dict via plugin options

![config window](/pluginspec/doc/tip/html/config.png)
"""


#import os
import re
#import json
import glob
import textwrap
import PySimpleGUI as sg
import pluginconf


# temporarily store collected plugin config: dicts
OPTIONS = {}


#-- show configuation window
def window(config, plugin_states, files=["*/*.py"], **kwargs):
    """
    Reads *.py files and crafts a settings dialog from meta data.

    Where `plugin_states{}` is usually an entry in `config{}` itself. Depending on plugin
    and option names, it might even be a flat/shared namespace for both. Per default you'd
    set `files=["plugins/*.py", __file__]` to be read. But with `files=[]` it's possible to
    provide a `plugins=pluginconf.get_plugin_meta()` or prepared plugin/options dict instead.

    | Params        | | |
    |---------------|---------|---------------------------------------------------------|
    | config        | dict 🔁 | Config settings, updated after dialog completion        |
    | plugin_states | dict 🔁 | Plugin activation states, also input/output             |
    | files         | list    | Glob list of *.py files to extract meta definitions from|
    | plugins       | dict    | Alternatively to files=[] list, a preparsed list of pluginmeta+config dicts can be injected |
    | opt_label     | bool    | Show config name= as label (instead of description)     |
    | theme         | str     | Set PSG window theme.                                   |
    | **kwargs      | dict    | Other options are passed on to PySimpleGUI              |
    | **Returns**   | True    | if updated config{} values should be [Saved]            |
    """
    plugins = kwargs.get("plugins", {})
    opt_label = kwargs.get("opt_label", False)
    theme = kwargs.get("theme", "DefaultNoMoreNagging")
    if theme:
        if "theme" in kwargs:
            del kwargs["theme"]
        sg.theme(theme)
    if files:
        plugins = read_options(files)
    layout = plugin_layout(plugins.values(), config, plugin_states, opt_label=opt_label)
    layout.append([sg.T(" ")])
    #print(repr(layout))

    # pack window
    layout = [
        [sg.Column(layout, expand_x=1, expand_y=0, size=(575, 680), scrollable="vertically", element_justification='left')],
        [sg.Column([[sg.Button("Cancel"), sg.Button("Save")]], element_justification='right')]
    ]
    if "title" not in kwargs:
        kwargs["title"] = "Options"
    if "font" not in kwargs:
        kwargs["font"] = "Sans 11"
    win = sg.Window(layout=layout, resizable=1, **kwargs)

    # wait for save/exit
    event, data = win.read()
    win.close()
    if event == "Save":
        for key, val in data.items():
            if OPTIONS.get(key):
                #@ToDo: handle array[key] names
                config[key] = Cast.fromtype(data[key], OPTIONS[key])
            elif isinstance(key, str) and key.startswith('p:'):
                key = key.replace('p:', '')
                if plugins.get(key):
                    plugin_states[key] = val
        return True
    #print(config, plugin_states)


def plugin_layout(pmd_list, config, plugin_states, opt_label=False):
    """ craft list of widgets: \*( `plugin_entry`, \*`option_entry` )"""
    layout = []
    for plg in pmd_list:
        #print(plg.get("id"))
        layout = layout + plugin_entry(plg, plugin_states)
        for opt in plg["config"]:
            if opt.get("name"):
                if opt_label:
                    layout.append([sg.T(opt["name"], font=("Sans", 11, "bold"), pad=((50, 0), (7, 0)))])
                layout.append(option_entry(opt, config))
    return layout

def plugin_entry(pmd, plugin_states):
    """ checkbox for plugin name """
    name = pmd["id"]
    return [
        [
            sg.Checkbox(
                pmd.get("title", name), key='p:'+name, default=plugin_states.get(name, 0),
                tooltip=pmd.get("doc"), metadata="plugin", font="bold", pad=(0, (8, 0))
            ),
            sg.Text("({}/{})".format(pmd.get("type"), pmd.get("category")), text_color="#005", pad=(0, (8, 0))),
            sg.Text(pmd.get("version"), text_color="#a72", pad=(0, (8, 0)))
        ],
        [
            sg.Text(pmd.get("description", ""), tooltip=pmd.get("doc"), font=("sans", 10), pad=(26, (0, 10)))
        ]
    ]

def option_entry(opt, config):
    """ widgets for single config option """
    #print(o)
    name = opt.get("name", "")
    desc = wrap(opt.get("description", name), 60)
    typedef = opt.get("type", "str")
    tooltip = wrap(opt.get("help", name), 60)
    OPTIONS[name] = opt
    val = config.get(name, opt.get("value", ""))

    widget = []
    if opt.get("hidden"):
        pass
    elif typedef == "str":
        widget = [
            sg.InputText(key=name, default_text=str(val), size=(20, 1), pad=((50, 0), 3)),
            sg.Text(wrap(desc, 50), pad=(5, 2), tooltip=tooltip, justification='left', auto_size_text=1)
        ]
    elif typedef == "text":
        widget = [
            sg.Multiline(key=name, default_text=str(val), size=(45, 4), pad=((40, 0), 3)),
            sg.Text(wrap(desc, 20), pad=(5, 2), tooltip=tooltip, justification='left', auto_size_text=1)
        ]
    elif typedef == "bool":
        widget = [
            sg.Checkbox(wrap(desc, 70), key=name, default=Cast.bool(val), tooltip=tooltip, pad=((40, 0), 2), auto_size_text=1)
        ]
    elif typedef == "int":
        widget = [
            sg.InputText(key=name, default_text=str(val), size=(6, 1), pad=((50, 0), 3)),
            sg.Text(wrap(desc, 60), pad=(5, 2), tooltip=tooltip, auto_size_text=1)
        ]
    elif typedef == "select":
        values = opt["select"].values()
        widget = [
            sg.Combo(key=name, default_value=opt["select"].get(val, val), values=values, size=(15, 1), pad=((50, 0), 0), font="Sans 11"),
            sg.Text(wrap(desc, 47), pad=(5, 2), tooltip=tooltip, auto_size_text=1)
        ]
    elif typedef == "dict":  # or "table" rather ?
        widget = [
            sg.Table(
                values=config.get(name, ["", ""]), headings=opt.get("columns", "Key,Value").split(","),
                num_rows=5, col_widths=30, def_col_width=30, auto_size_columns=False, max_col_width=150,
                key=name, tooltip=wrap(opt.get("help", desc))
            )
        ]
    return widget


def read_options(files):
    """ read files, return dict of {id:pmd} for all plugins """
    return {
        meta["id"]: meta for meta in
        [pluginconf.plugin_meta(fn=fn) for pattern in files for fn in glob.glob(pattern)]
    }


class Cast:
    """ map option types (from strings) """

    @staticmethod
    def bool(val):
        """ map boolean literals """
        if val in ("1", 1, True, "true", "TRUE", "yes", "YES", "on", "ON"):
            return True
        return False

    @staticmethod
    def int(val):
        """ verify integer """
        return int(val) if re.match(r"-?\d+", val) else 0

    @staticmethod
    def fromtype(val, opt):
        """ cast according to option type """
        if not opt.get("type"):
            return str(val)
        if opt["type"] == "int":
            return Cast.int(val)
        if opt["type"] == "bool":
            return Cast.bool(val)
        if opt["type"] == "select":
            inverse = dict((val, key) for key, val in opt["select"].items())
            return inverse.get(val, val)
        if opt["type"] == "text":
            return str(val).rstrip()
        # else:
        return val

def wrap(text, width=50):
    """ textwrap for `description` and `help` option fields """
    return "\n".join(textwrap.wrap(text, width)) if text else ""
