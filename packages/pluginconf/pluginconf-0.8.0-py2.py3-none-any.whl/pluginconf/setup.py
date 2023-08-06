# encoding: utf-8
# api: setuptools
##type: functions
# title: setup() wrapper
# description: utilizes PMD to populate some package fields
# version: 0.5
# license: PD
# permissive: 0.3
# pylint: disable=line-too-long
#
# Utilizes plugin meta data to cut down setup.py incantations
# to basically just:
#
#     from pluginconf.setup import setup
#     setup(
#         fn="pluginconf/__init__.py"
#     )
#
# Where the fn= either pinpoints the main invocation point,
# when name= or packages= (implicitly from `find_packages()`)
# don't specify a locatable script already.
#
# Mapped meta fields include:
#
#     # description: …
#     # version: …
#     # url: …
#     # depends: python (>= 2.7), python:pkg-name (>= 1.0)
#     # suggests: python:extras_require (>= 1.0)
#     # author: …
#     # license: spdx
#     # state: stable
#     # type: classifier
#     # category: classifier
#     # keywords: tag, tag
#     # classifiers: tag, trove, shortcuts
#     # doc-format: text/markdown
#     #
#     # Long description used in lieu of README...
#
# A README.* will be read if present, else PMD comment used.
# Classifiers and license matching is very crude, just for
# the most common cases. Type:, Category: and Classifiers:
# or Keywords: are also scanned for trove classifers.
#

""" Expands setuptools.setup() with automatic package description lookup """


import os
import re
import glob
import pprint
import pluginconf


def name_to_fn(name):
    """ find primary entry point.py from package name """
    for pfx in "", "src/", "src/"+name+"/":
        for sfx in ".py", "/__init__.py":
            if os.path.exists(pfx+name+sfx):
                return pfx+name+sfx
    return ""

def get_readme():
    """ get README.md contents """
    for filename, mime in ("README.md", "text/markdown"), ("README.rst", "text/x-rst"), ("README.txt", "text/plain"):
        if os.path.exists(filename):
            with open(filename, "r") as read:
                return {
                    "long_description": read.read(),
                    "long_description_content_type": mime,
                }
    return {
        "long_description": "",
        "long_description_content_type": "text/plain",
    }


class MetaUtils(dict):
    """ Convenience access to PMD fields and conversion functions """

    def __getattr__(self, name):
        """ dict into properties """
        return self.get(name, "")

    def plugin_doc(self):
        """ use comment block """
        return {
            "long_description": self.doc,
            "long_description_content_type": self.doc_format or "text/plain"
        }

    def python_requires(self):
        """ depends: python >= 3.5 """
        deps = re.findall(r"python\s*\(?(>=?\s?[\d.]+)", self.get("depends", ""))
        if deps:
            return deps[0]
        return None

    def install_requires(self):
        """ depends: python:module, pip:module """
        deps = re.findall(r"(?:python|pip):([\w\-]+)\s*([<!=>\s\d\w.\-~]+|\([<!=>\s\d\w.\-,~]+\))?", self.get("depends", ""))
        if deps:
            for index, (name, ver) in enumerate(deps):
                ver = re.sub(r"[(\s)]+", "", ver)
                if not ver:
                    continue
                ver = re.sub("(,)", r"\1 ", ver)
                deps[index] = (name, " (" + ver + ")")
            # doesn't need much cleanup: https://peps.python.org/pep-0508/
            return [name + ver for name, ver in deps]
        return []

    def extras_require(self):
        """ suggest: line """
        deps = re.findall(r"(?:python|pip):([\w\-]+)\s*\(?\s*([>=<]+\s*[\d.\-]+)", self.get("suggests", ""))
        if deps:
            return dict(deps)
        return {}

    def project_urls(self, exclude=("url", "update",)):
        """ other-url: https://... """
        urls = {}
        for key, url in self.items():
            if isinstance(url, str) and key not in exclude and re.match(r"https?://\S+", url):
                urls[key.title()] = url
        return urls

    def classifiers(self):
        """ classifiers: / keywords: / category: """
        for field in ("api", "category", "type", "keywords", "classifiers"):
            field = self.get(field, "")
            field = re.findall(r"(\w{4,})", field)
            regex = "|".join(field)
            if not regex:
                continue
            for line in TOPIC_TROVE:
                if re.search("::[^:]*("+regex+")[^:]*$", line, re.I):
                    yield line

    def trove_license(self):
        """ license: to License :: """
        trove_licenses = {
            r"MITL?": "License :: OSI Approved :: MIT License",
            r"\bPD\b|CC-?0|Public ?Domain|Unlicense": "License :: Public Domain",
            r"ASL": "License :: OSI Approved :: Apache Software License",
            r"art": "License :: OSI Approved :: Artistic License",
            r"BSDL?": "License :: OSI Approved :: BSD License",
            r"CPL": "License :: OSI Approved :: Common Public License",
            r"AGPL.*3": "License :: OSI Approved :: GNU Affero General Public License v3",
            r"AGPLv*3\+": "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            r"\bGPL": "License :: OSI Approved :: GNU General Public License (GPL)",
            r"\bGPL.*3": "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            r"LGPL": "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
            r"MPL": "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            r"Pyth": "License :: OSI Approved :: Python Software Foundation License"
        }
        for regex, trove in trove_licenses.items():
            if re.search(regex, self.license, re.I):
                return [trove]
        return []

    def trove_status(self):
        """ state: to DevStatus :: """
        trove_status = {
            "pre|release|cand": "Development Status :: 2 - Pre-Alpha",
            "alpha": "Development Status :: 3 - Alpha",
            "beta": "Development Status :: 4 - Beta",
            "stable": "Development Status :: 5 - Production/Stable",
            "mature": "Development Status :: 6 - Mature"
        }
        for regex, trove in trove_status.items():
            state = self.state or self.status or "alpha"
            if re.search(regex, state, re.I):
                return [trove]
        return []

    @staticmethod
    def datafiles_man():
        """ data_files= """
        for man in glob.glob("man*/*.[12345678]"):
            section = man[-1]
            yield ("man/man"+section, [man],)

    def entry_points(self):
        """ collect console-scripts: """
        params = {}
        for field in ["console_scripts", "gui_scripts"]:
            if not self.get(field):
                continue
            params[field] = params.get(field, []) + re.findall(r"(\w+[^,;\s]+=\w+[^,;\s]+)", self[field])
        return params

    def get_keywords(self):
        """ keywords= """
        return self.keywords or self.category or self.type


@pluginconf.renamed_arguments({"fn": "filename"})
def setup(filename=None, debug=False, **kwargs):
    """
    Wrapper around `setuptools.setup()` which adds some defaults
    and plugin meta data import, with some shortcut parameters:

    | Parameters  | | |
    |-------------|--------|------------------------------------------------|
    | filename    | str    | main file "pkg/main.py" (else deduced from primary package name) |
    | debug       | bool   | display collected options prior setuptools.setup() invocation |
    |long_description| str | e.g. "README.md", else the comment block gets used |

    Other setup() params work as usual, and are passed trough. Notably
    entry_points= or data_files= can be used, even if they get augmented.
    """

    # optionalized here (avoid dependency in flit import)
    # p-y-l-i-n-t: disable=import-outside-toplevel
    import setuptools

    # stub values
    stub = {
        "classifiers": [],
        "project_urls": {},
        "python_requires": ">= 2.7",
        "install_requires": [],
        "extras_require": {},
        #"package_dir": {"": "."},
        #"package_data": {},
        #"data_files": [],
        "entry_points": {},
        "packages": setuptools.find_packages()
    }
    for key, val in stub.items():
        if not key in kwargs:
            kwargs[key] = val

    # package name
    if "name" not in kwargs and kwargs.get("packages"):
        kwargs["name"] = kwargs["packages"][0]

    # read README if field empty or says `@README`
    if re.match("^$|^[@./]*README.{0,5}$", kwargs.get("long_description", "")):
        kwargs.update(get_readme())

    # search name= package if no filename= given
    if not filename and kwargs.get("name"):
        filename = name_to_fn(kwargs["name"])

    # read plugin meta data (PMD)
    pmd = MetaUtils(
        pluginconf.plugin_meta(filename=filename)
    )

    # use id: if no name= still
    if pmd.get("id") and not kwargs.get("name"):
        if pmd["id"] == "__init__":
            pmd["id"] = re.findall(r"([\w\.\-]+)/__init__.+$", filename)[0]
        kwargs["name"] = pmd["id"]

    # version:, description:, author:
    for field in "version", "description", "license", "author", "url":
        if field in pmd and not field in kwargs:
            kwargs[field] = pmd[field]

    # other urls:
    kwargs["project_urls"].update(pmd.project_urls())
    # depends:
    if "depends" in pmd:
        kwargs["python_requires"] = pmd.python_requires()
    if "depends" in pmd and not kwargs["install_requires"]:
        kwargs["install_requires"] = pmd.install_requires()
    # suggests:
    if "suggests" in pmd and not kwargs["extras_require"]:
        kwargs["extras_require"].update(pmd.extras_require())
    # doc:
    if not kwargs.get("long_description"):
        kwargs.update(pmd.plugin_doc())

    # keywords=
    if "keywords" not in kwargs:
        kwargs["keywords"] = pmd.get_keywords()

    # automatic inclusions
    kwargs["data_files"] = kwargs.get("data_files", []) + list(pmd.datafiles_man())
    # entry points
    for section, entries in pmd.entry_points().items():
        kwargs["entry_points"][section] = kwargs["entry_points"].get(section, []) + entries

    # classifiers=
    # license:
    if pmd.get("license") and not any(re.match("License ::", l) for l in kwargs["classifiers"]):
        kwargs["classifiers"].extend(pmd.trove_license())
    # state:
    if pmd.get("state", pmd.get("status")) and not any(re.match("Development Status ::", l) for l in kwargs["classifiers"]):
        kwargs["classifiers"].extend(pmd.trove_status())
    # topics::
    kwargs["classifiers"].extend(list(pmd.classifiers()))

    # handover
    if debug:
        pprint.pprint(kwargs)
    setuptools.setup(**kwargs)



TOPIC_TROVE = """Topic :: Adaptive Technologies
Topic :: Artistic Software
Topic :: Communications
Topic :: Communications :: BBS
Topic :: Communications :: Chat
Topic :: Communications :: Chat :: ICQ
Topic :: Communications :: Chat :: Internet Relay Chat
Topic :: Communications :: Chat :: Unix Talk
Topic :: Communications :: Conferencing
Topic :: Communications :: Email
Topic :: Communications :: Email :: Address Book
Topic :: Communications :: Email :: Email Clients (MUA)
Topic :: Communications :: Email :: Filters
Topic :: Communications :: Email :: Mail Transport Agents
Topic :: Communications :: Email :: Mailing List Servers
Topic :: Communications :: Email :: Post-Office
Topic :: Communications :: Email :: Post-Office :: IMAP
Topic :: Communications :: Email :: Post-Office :: POP3
Topic :: Communications :: FIDO
Topic :: Communications :: Fax
Topic :: Communications :: File Sharing
Topic :: Communications :: File Sharing :: Gnutella
Topic :: Communications :: File Sharing :: Napster
Topic :: Communications :: Ham Radio
Topic :: Communications :: Internet Phone
Topic :: Communications :: Telephony
Topic :: Communications :: Usenet News
Topic :: Database :: Database Engines/Servers
Topic :: Database :: Front-Ends
Topic :: Desktop Environment :: File Managers
Topic :: Desktop Environment :: GNUstep
Topic :: Desktop Environment :: Gnome
Topic :: Desktop Environment :: K Desktop Environment (KDE)
Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes
Topic :: Desktop Environment :: PicoGUI
Topic :: Desktop Environment :: PicoGUI :: Applications
Topic :: Desktop Environment :: PicoGUI :: Themes
Topic :: Desktop Environment :: Screen Savers
Topic :: Documentation :: Sphinx
Topic :: Education
Topic :: Education :: Computer Aided Instruction (CAI)
Topic :: Education :: Testing
Topic :: Games/Entertainment
Topic :: Games/Entertainment :: Arcade
Topic :: Games/Entertainment :: Board Games
Topic :: Games/Entertainment :: First Person Shooters
Topic :: Games/Entertainment :: Fortune Cookies
Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)
Topic :: Games/Entertainment :: Puzzle Games
Topic :: Games/Entertainment :: Real Time Strategy
Topic :: Games/Entertainment :: Role-Playing
Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games
Topic :: Games/Entertainment :: Simulation
Topic :: Games/Entertainment :: Turn Based Strategy
Topic :: Home Automation
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: Finger
Topic :: Internet :: Log Analysis
Topic :: Internet :: Name Service (DNS)
Topic :: Internet :: Proxy Servers
Topic :: Internet :: WAP
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Dynamic Content
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters
Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki
Topic :: Internet :: WWW/HTTP :: HTTP Servers
Topic :: Internet :: WWW/HTTP :: Indexing/Search
Topic :: Internet :: WWW/HTTP :: Session
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Internet :: WWW/HTTP :: WSGI
Topic :: Internet :: WWW/HTTP :: WSGI :: Application
Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware
Topic :: Internet :: WWW/HTTP :: WSGI :: Server
Topic :: Internet :: XMPP
Topic :: Internet :: Z39.50
Topic :: Multimedia
Topic :: Multimedia :: Graphics
Topic :: Multimedia :: Graphics :: 3D Modeling
Topic :: Multimedia :: Graphics :: 3D Rendering
Topic :: Multimedia :: Graphics :: Capture
Topic :: Multimedia :: Graphics :: Capture :: Digital Camera
Topic :: Multimedia :: Graphics :: Capture :: Scanners
Topic :: Multimedia :: Graphics :: Capture :: Screen Capture
Topic :: Multimedia :: Graphics :: Editors
Topic :: Multimedia :: Graphics :: Editors :: Raster-Based
Topic :: Multimedia :: Graphics :: Editors :: Vector-Based
Topic :: Multimedia :: Graphics :: Graphics Conversion
Topic :: Multimedia :: Graphics :: Presentation
Topic :: Multimedia :: Graphics :: Viewers
Topic :: Multimedia :: Sound/Audio
Topic :: Multimedia :: Sound/Audio :: Analysis
Topic :: Multimedia :: Sound/Audio :: CD Audio
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping
Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing
Topic :: Multimedia :: Sound/Audio :: Capture/Recording
Topic :: Multimedia :: Sound/Audio :: Conversion
Topic :: Multimedia :: Sound/Audio :: Editors
Topic :: Multimedia :: Sound/Audio :: MIDI
Topic :: Multimedia :: Sound/Audio :: Mixers
Topic :: Multimedia :: Sound/Audio :: Players
Topic :: Multimedia :: Sound/Audio :: Players :: MP3
Topic :: Multimedia :: Sound/Audio :: Sound Synthesis
Topic :: Multimedia :: Sound/Audio :: Speech
Topic :: Multimedia :: Video
Topic :: Multimedia :: Video :: Capture
Topic :: Multimedia :: Video :: Conversion
Topic :: Multimedia :: Video :: Display
Topic :: Multimedia :: Video :: Non-Linear Editor
Topic :: Office/Business
Topic :: Office/Business :: Financial
Topic :: Office/Business :: Financial :: Accounting
Topic :: Office/Business :: Financial :: Investment
Topic :: Office/Business :: Financial :: Point-Of-Sale
Topic :: Office/Business :: Financial :: Spreadsheet
Topic :: Office/Business :: Groupware
Topic :: Office/Business :: News/Diary
Topic :: Office/Business :: Office Suites
Topic :: Office/Business :: Scheduling
Topic :: Other/Nonlisted Topic
Topic :: Printing
Topic :: Religion
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Artificial Intelligence
Topic :: Scientific/Engineering :: Artificial Life
Topic :: Scientific/Engineering :: Astronomy
Topic :: Scientific/Engineering :: Atmospheric Science
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)
Topic :: Scientific/Engineering :: GIS
Topic :: Scientific/Engineering :: Human Machine Interfaces
Topic :: Scientific/Engineering :: Hydrology
Topic :: Scientific/Engineering :: Image Processing
Topic :: Scientific/Engineering :: Image Recognition
Topic :: Scientific/Engineering :: Information Analysis
Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Medical Science Apps.
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Visualization
Topic :: Security
Topic :: Security :: Cryptography
Topic :: Sociology
Topic :: Sociology :: Genealogy
Topic :: Sociology :: History
Topic :: Software Development
Topic :: Software Development :: Assemblers
Topic :: Software Development :: Bug Tracking
Topic :: Software Development :: Build Tools
Topic :: Software Development :: Code Generators
Topic :: Software Development :: Compilers
Topic :: Software Development :: Debuggers
Topic :: Software Development :: Disassemblers
Topic :: Software Development :: Documentation
Topic :: Software Development :: Embedded Systems
Topic :: Software Development :: Internationalization
Topic :: Software Development :: Interpreters
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Application Frameworks
Topic :: Software Development :: Libraries :: Java Libraries
Topic :: Software Development :: Libraries :: PHP Classes
Topic :: Software Development :: Libraries :: Perl Modules
Topic :: Software Development :: Libraries :: Pike Modules
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Libraries :: Ruby Modules
Topic :: Software Development :: Libraries :: Tcl Extensions
Topic :: Software Development :: Libraries :: pygame
Topic :: Software Development :: Localization
Topic :: Software Development :: Object Brokering
Topic :: Software Development :: Object Brokering :: CORBA
Topic :: Software Development :: Pre-processors
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Acceptance
Topic :: Software Development :: Testing :: BDD
Topic :: Software Development :: Testing :: Mocking
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: Software Development :: Testing :: Unit
Topic :: Software Development :: User Interfaces
Topic :: Software Development :: Version Control
Topic :: Software Development :: Version Control :: Bazaar
Topic :: Software Development :: Version Control :: CVS
Topic :: Software Development :: Version Control :: Git
Topic :: Software Development :: Version Control :: Mercurial
Topic :: Software Development :: Version Control :: RCS
Topic :: Software Development :: Version Control :: SCCS
Topic :: Software Development :: Widget Sets
Topic :: System
Topic :: System :: Archiving
Topic :: System :: Archiving :: Backup
Topic :: System :: Archiving :: Compression
Topic :: System :: Archiving :: Mirroring
Topic :: System :: Archiving :: Packaging
Topic :: System :: Benchmark
Topic :: System :: Boot
Topic :: System :: Boot :: Init
Topic :: System :: Clustering
Topic :: System :: Console Fonts
Topic :: System :: Distributed Computing
Topic :: System :: Emulators
Topic :: System :: Filesystems
Topic :: System :: Hardware
Topic :: System :: Hardware :: Hardware Drivers
Topic :: System :: Hardware :: Mainframes
Topic :: System :: Hardware :: Symmetric Multi-processing
Topic :: System :: Installation/Setup
Topic :: System :: Logging
Topic :: System :: Monitoring
Topic :: System :: Networking
Topic :: System :: Networking :: Firewalls
Topic :: System :: Networking :: Monitoring
Topic :: System :: Networking :: Monitoring :: Hardware Watchdog
Topic :: System :: Networking :: Time Synchronization
Topic :: System :: Operating System
Topic :: System :: Operating System Kernels
Topic :: System :: Operating System Kernels :: BSD
Topic :: System :: Operating System Kernels :: GNU Hurd
Topic :: System :: Operating System Kernels :: Linux
Topic :: System :: Power (UPS)
Topic :: System :: Recovery Tools
Topic :: System :: Shells
Topic :: System :: Software Distribution
Topic :: System :: System Shells
Topic :: System :: Systems Administration
Topic :: System :: Systems Administration :: Authentication/Directory
Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP
Topic :: System :: Systems Administration :: Authentication/Directory :: NIS
Topic :: Terminals
Topic :: Terminals :: Serial
Topic :: Terminals :: Telnet
Topic :: Terminals :: Terminal Emulators/X Terminals
Topic :: Text Editors
Topic :: Text Editors :: Emacs
Topic :: Text Editors :: Integrated Development Environments (IDE)
Topic :: Text Editors :: Text Processing
Topic :: Text Editors :: Word Processors
Topic :: Text Processing
Topic :: Text Processing :: Filters
Topic :: Text Processing :: Fonts
Topic :: Text Processing :: General
Topic :: Text Processing :: Indexing
Topic :: Text Processing :: Linguistic
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: LaTeX
Topic :: Text Processing :: Markup :: Markdown
Topic :: Text Processing :: Markup :: SGML
Topic :: Text Processing :: Markup :: VRML
Topic :: Text Processing :: Markup :: XML
Topic :: Text Processing :: Markup :: reStructuredText
Topic :: Utilities""".split(r"\n")

try:
    from trove_classifiers import classifiers
    TOPIC_TROVE = [line for line in classifiers if re.match("Topic ::", line)]
except:
    pass
