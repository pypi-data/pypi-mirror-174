# static/setup_files.py
from pathlib import Path

import ujson as json
from rich import print
from rich.panel import Panel
from rich.style import Style
from rich.table import Table, Column
from sh import Command


from maxsetup.console import console, progress

BASE = Path.cwd()
LICENSE_FILEPATH = BASE / "LICENSE"  # 1
GITIGNORE_FILEPATH = BASE / ".gitignore"  # 2
DOTENV_FILEPATH = BASE / ".env"
VSCODE_DIR = BASE / ".vscode"
LAUNCH_FILEPATH = VSCODE_DIR / "launch.json"  # 3
SETTINGS_FILEPATH = VSCODE_DIR / "settings.json"  # 4
TASKS_FILEPATH = VSCODE_DIR / "tasks.json"  # 5
STATIC_DIR = BASE / "static"
CSS_FILEPATH = STATIC_DIR / "style.css"  # 6
CONFIG_DIR = BASE / "config"
CSPELL_FILEPATH = CONFIG_DIR / "cspell.json"  # 7
LOGS_DIR = BASE / "logs"
RUN_FILEPATH = LOGS_DIR / "run.text"  # 8
LOG_FILEPATH = LOGS_DIR / "log.log"  # 9
VERBOSE_LOG_FILEPATH = LOGS_DIR / "verbose.log"  # 10
TASKS_DIR = BASE / "tasks"

DIRS = [BASE, CONFIG_DIR, LOGS_DIR, STATIC_DIR, VSCODE_DIR, TASKS_DIR]

FONTS = [
    "Century Gothic Bold.ttf",
    "Century Gothic.ttf",
    "MesloLGS NF Bold Italic.ttf",
    "MesloLGS NF Bold.ttf",
    "MesloLGS NF Italic.ttf",
    "MesloLGS NF Regular.ttf",
    "Urbanist-Black.ttf",
    "Urbanist-BlackItalic.ttf",
    "Urbanist-Italic.ttf",
    "Urbanist-Light.ttf",
    "Urbanist-LightItalic.ttf",
    "Urbanist-Regular.ttf",
    "White Modesty.ttf",
]

FILES = [
    {
        "file": "launch.json",
        "type": "json",
        "filepath": LAUNCH_FILEPATH,
        "content": """{\n\t\"version\": \"0.2.0\",\n\t\"configurations\": [\n\t\t{\n\t\t\t\"name\": \"Python: Current File\",\n\t\t\t\"type\": \"python\",\n\t\t\t\"request\": \"launch\",\n\t\t\t\"program\": \"${file}\",\n\t\t\t\"console\": \"integratedTerminal\",\n\t\t\t\"justMyCode\": true\n\t\t}\n\t]\n}""",
    },
    {
        "file": "settings.json",
        "type": "json",
        "filepath": f"{BASE}/.vscode/settings.json",
        "content": """{\n\t\"files.trimFinalNewlines\": true,\n\t\"files.trimTrailingWhitespace\": true,\n\t\"breadcrumbs.showModules\": true,\n\t\"markdown.preview.fontFamily\": \"\'Century Gothic\',\' MesloLGS NF\', \'Ubuntu\', sans-serif\",\n\t\"editor.fontFamily\": \"\'MesloLGS NF\', Menlo, Monaco, \'Courier New\', monospace\",\n\t\"editor.fontSize\": 14,\n\t\"editor.formatOnSave\": true,\n\t\"cSpell.customDictionaries\": {\n\t\t\"project-words\": {\n\t\t\t\"name\": \"cspell\",\n\t\t\t\"path\": \"${workspaceRoot}/config/cspell.txt\",\n\t\t\t\"description\": \"Words used in the configured project.\",\n\t\t\t\"addWords\": true\n\t\t}\n\t},\n\t\"[python]\": {\n\t\t\"editor.defaultFormatter\": \"ms-python.python\"\n\t}\n}""",
    },
    {
        "file": "tasks.json",
        "type": "json",
        "filepath": f"{BASE}/.vscode/tasks.json",
        "content": """{\n\t\"version\": \"2.0.0\",\n\t\"tasks\": [\n\t\t{\n\t\t\t\"label\": \"Setup Files\",\n\t\t\t\"command\": \"/Users/maxludden/dev/venvs/maxsetup/bin/python /Users/maxludden/dev/py/maxsetup/setup_files.py\",\n\t\t\t\"type\": \"shell\",\n\t\t\t\"group\": {\n\t\t\t\t\"kind\": \"none\",\n\t\t\t\t\"isDefault\": false\n\t\t\t},\n\t\t\t\"presentation\": {\n\t\t\t\t\"echo\": false,\n\t\t\t\t\"reveal\": \"always\",\n\t\t\t\t\"focus\": false,\n\t\t\t\t\"panel\": \"shared\",\n\t\t\t\t\"showReuseMessage\": true,\n\t\t\t\t\"clear\": false\n\t\t\t},\n\t\t\t\"icon\": {\n\t\t\t\t\"id\": \"symbol-type-parameter\",\n\t\t\t\t\"color\": \"terminal.ansiCyan\"\n\t\t\t},\n\t\t\t\"runOptions\": {\n\t\t\t\t\"runOn\": \"default\",\n\t\t\t\t\"instanceLimit\": 1,\n\t\t\t\t\"reevaluateOnRerun\": true\n\t\t\t}\n\t\t}\n\t]\n}""",
    },
    {
        "file": "cspell.json",
        "type": "json",
        "filepath": f"{BASE}/config/cspell.json",
        "content": """{\n\t\"version\": \"0.2\",\n\t\"ignorePaths\": [],\n\t\"dictionaryDefinitions\": [\n\t\t{\n\t\t\t\"name\": \"cspell\",\n\t\t\t\"path\": \"${workspaceRoot}/config/cspell.txt\",\n\t\t\t\"description\": \"Custom words for cspell\",\n\t\t\t\"type\": \"S\",\n\t\t\t\"addWords\": true,\n\t\t\t\"useCompounds\": true,\n\t\t\t\"scope\": \"folder\"\n\t\t}\n\t],\n\t\"dictionaries\": [],\n\t\"words\": [],\n\t\"ignoreWords\": [],\n\t\"import\": []\n}\n""",
    },
    {
        "file": "cspell.txt",
        "type": "text",
        "filepath": f"{BASE}/config/cspell.txt",
        "content": "adipisicing\naliqua\naliquip\namet\naute\nAute\ncillum\nCKRE\ncommodo\nconsectetur\nConsectetur\nconsequat\ncupidatat\nCupidatat\ndeserunt\ndolore\nduis\neiusmod\nEiusmod\nelit\nexcepteur\nfugiat\nFugiat\ngradiented\nhhyfx\nincididunt\nirure\nkxoynn\nlabore\nlaboris\nlaborum\nMenlo\nmollit\nnostrud\nnulla\noccaecat\nofficia\npariatur\nproident\nquis\nrainbowed\nRenderable\nsunt\nSunt\ntempor\nTize\nudvr\nullamco\nvelit\nveniam\nvoluptate\nVoluptate\nykexju\n",
    },
    {
        "file": "run.txt",
        "type": "text",
        "filepath": f"{BASE}/logs/run.txt",
        "content": """0""",
    },
    {
        "file": "style.css",
        "type": "text",
        "filepath": f"{BASE}/static/style.css",
        "content": '@charset "utf-8";\n\n/* This stylesheet was created by Max Ludden to use for ebooks I created. Like everything else in this module, it is under the MIT License, so use it if you like it. */\n:root {\n\t--main-color: #000000;\n\t--main-bg-color: #ffffff;\n\t--main-border-color: #bbbbbb;\n\t--alternate-color: #222222;\n\t--alternate-bg-color: #efefef;\n\t--alternate-border-color: #2e2e2e;\n\t--table-header-bg-color: #222222;\n\t--link-color: #61008e;\n\t--title-color: #61008e;\n}\n\n@media (prefers-color-scheme: dark) {\n\t:root {\n\t\t--main-color: #eeeeee;\n\t\t--main-bg-color: #222222;\n\t\t--main-border-color: #aaaaaa;\n\t\t--alternate-color: #dddddd;\n\t\t--alternate-bg-color: #444444;\n\t\t--alternate-border-color: #2e2e2e;\n\t\t--table-header-bg-color: #aaaaaa;\n\t\t--link-color: #61008e;\n\t\t--title-color: #d98eff;\n\t}\n}\n\n/**** Fonts *******/\n@font-face {\n\tfont-family: "Urbanist-Thin";\n\tfont-style: normal;\n\tsrc: "Urbanist-Thin.ttf"\n}\n\n@font-face {\n\tfont-family: "Urbanist-ThinItalic";\n\tfont-style: normal;\n\tsrc: "Urbanist-thinItalic.ttf"\n}\n\n@font-face {\n\tfont-family: "Urbanist-Regular";\n\tfont-style: normal;\n\tsrc: "Urbanist-Regular.ttf"\n}\n\n@font-face {\n\tfont-family: "Urbanist-Italic";\n\tfont-style: italic;\n\tsrc: "Urbanist-Italic.ttf"\n}\n\n@font-face {\n\tfont-family: "Urbanist-Black";\n\tfont-style: normal;\n\tfont_weight: bold;\n\tsrc: "Urbanist-Black.ttf"\n}\n\n@font-face {\n\tfont-family: "Urbanist-BlackItalic";\n\tfont-style: normal;\n\tfont_weight: bold;\n\tsrc: "Urbanist-BlackItalic.ttf"\n}\n\n@font-face {\n\tfont-family: "White Modesty";\n\tfont-style: normal;\n\tsrc: "White Modesty.ttf" ";\n\n}\n\n@font-face {\n\tfont-family: "MesloLGS NF Regular";\n\tfont-style: normal;\n\tsrc: "MesloLGS NF Regular.ttf";\n}\n\n@font-face {\n\tfont-family: "MesloLGS NF Italic";\n\tfont-style: italic;\n\tsrc: "MesloLGS NF Italic.ttf";\n}\n\n@font-face {\n\tfont-family: "MesloLGS NF Bold";\n\tfont-style: normal;\n\tfont-weight: bold;\n\tsrc: "MesloLGS NF Bold.ttf";\n}\n\n@font-face {\n\tfont-family: "MesloLGS NF Bold Italic";\n\tfont-style: italic;\n\tfont-weight: bold;\n\tsrc: "MesloLGS NF Bold Italic.ttf";\n}\n\n@font-face {\n\tfont-family: "Century Gothic";\n\tfont-style: normal;\n\tsrc: "Century Gothic.ttf";\n}\n\n@font-face {\n\tfont-family: "Century Gothic Bold";\n\tfont-style: italic;\n\tsrc: "Century Gothic Bold.ttf";\n}\n\n/***** End of Fonts **********/\n\nhtml {\n\tfont-size: 1em;\n\tfont-family: "Urbanist-Regular", "Century Gothic" -apple-system, BlinkMacSystemFont, "helvetica neue", helvetica, roboto, noto, "segoe ui", arial, sans-serif;\n\tline-height: 1.2em;\n\tbackground-color: var(--main-bg-color);\n\tcolor: var(--main-color);\n}\n\n/****** Headers *********/\nh1,\nh2,\nh3,\nh4,\nh5 {\n\tdisplay: block;\n\ttext-align: center;\n\tfont-family: "Urbanist-Regular", "Myriad Pro", helvetica, sans-serif;\n\tfont-style: normal;\n}\n\nh1 {\n\tfont-size: 1.5em;\n\tline-height: 1.2em;\n}\n\nh2 {\n\tfont-size: 1.25em;\n\tline-height: 1.1em;\n\tcolor: var(--alternate-color);\n}\n\nh3 {\n\tfont-size: 1.1em;\n\tline-height: 1em;\n\tfont-family: "Urbanist-Thin", "Myriad Pro", helvetica, sans-serif;\n\tcolor: var(--title-color);\n}\n\nh4 {\n\tfont-size: 1.1em;\n\tline-height: 1em;\n\tfont-family: "Urbanist-ThinItalic", "Myriad Pro", helvetica, sans-serif;\n\tcolor: var(--alternate-color);\n}\n\nh5 {\n\tfont-size: 0.9em;\n\tline-height: 1;\n}\n\n/* End of Headers */\n\n/****** Images *********/\nimg {\n\tdisplay: block;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\n/****** End of Images *********/\n\n/************** Body ***************/\nbody {\n\tmargin: 0;\n\tpadding: 1em;\n\tbackground-color: var(--main-bg-color);\n\tcolor: var(--main-color);\n\t-webkit-hyphenate-limit-before: 3;\n\t-webkit-hyphenate-limit-after: 2;\n\t-ms-hyphenate-limit-chars: 6 3 2;\n\t-webkit-hyphenate-limit-lines: 2;\n}\n\n/*********** @media ***********/\n@media(min-width: 390px) {\n\tbody {\n\t\tmargin: auto;\n\t}\n}\n\ntable {\n\tdisplay: table;\n\twidth: 95%;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tborder: 1px solid var(--main-border-color);\n\tborder-collapse: collapse;\n}\n\nth {\n\tpadding: .5em;\n\tcolor: var(--main-bg-color);\n\tbackground: var(--table-header-bg-color);\n\tfont-family: "Urbanist-Black", "Lemon/Milk", "Myriad Pro", helvetica, sans-serif;\n\tfont-size: 1.5em;\n\ttext-align: center;\n\tborder: 1px solid var(--main-border-color);\n}\n\ntd {\n\tfont-size: 1em;\n\tpadding: 10px;\n\tborder: 1px solid var(--main-border-color);\n\tborder-collapse: collapse;\n\tfont-family: "Urbanist-Regular", "Myriad Pro", helvetica, sans-serif;\n\ttext-align: center;\n}\n\n.status {\n\tborder: 1px solid var(--main-border-color);\n}\n\n.status td:nth-child(1) {\n\ttext-align: left;\n}\n\n.status td:nth-child(2) {\n\ttext-align: right;\n}\n\n.status tr:nth-child(odd) {\n\tbackground-color: var(--alternate-bg-color);\n}\n\n.status1 {\n\tborder: none;\n}\n\n.status1 td:nth-child(1) {\n\ttext-align: left;\n}\n\n.status1 td:nth-child(2) {\n\ttext-align: right;\n}\n\n.status1 tr:nth-child(odd) {\n\tbackground-color: var(--alternate-bg-color);\n}\n\n.class {\n\ttext-align: center;\n\tfont-family: Urbanist-Thin, Urbanist-Regular, "Myriad Pro", helvetica, sans-serif;\n\tfont-size: 0.8em;\n\tbackground-color: var(--main-bg-color);\n\tcolor: var(--main-color);\n\tborder: 1px solid var(--main-border-color);\n}\n\n.geno-r {\n\tborder: 1px solid var(--main-border-color);\n}\n\n.geno-r td:nth-child(1) {\n\ttext-align: left;\n}\n\n.geno-r td:nth-child(2) {\n\ttext-align: right;\n}\n\n.geno {\n\tborder: var(--main-border-color);\n}\n\n.geno td:nth-child(odd) {\n\ttext-align: left;\n}\n\n.geno td:nth-child(even) {\n\ttext-align: right;\n}\n\n.geno tr:nth-child(even) {\n\tbackground-color: var(--alternate-bg-color);\n}\n\n.beast {\n\tborder: none;\n\tborder-top: none;\n\tborder-bottom: none;\n}\n\n.beast td {\n\ttext-align: center;\n}\n\n.type {\n\ttext-align: center;\n\tfont-family: Urbanist-Thin, Urbanist-Regular, "Myriad Pro", helvetica, sans-serif;\n\tfont-size: 0.8em;\n\tborder: none;\n}\n\n.beast tr:nth-child(even) {\n\tbackground-color: var(--alternate-bg-color);\n}\n\n.article-reply {\n\twidth: 70%;\n\tpadding: 1.5em;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tcolor: var(--alternate-color);\n\tbackground-color: var(--alternate-bg-color);\n\tfont-family: Urbanist-Italic;\n\tborder: 1px solid var(--alternate-color);\n\tborder-radius: 5%;\n}\n\n.article {\n\twidth: 70%;\n\tpadding: 1.5em;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tcolor: var(--alternate-color);\n\tbackground-color: var(--alternate-bg-color);\n\tfont-family: Urbanist-Italic;\n\tborder: 1px solid var(--alternate-color);\n\tborder-radius: 5%;\n}\n\n.alert {\n\tpadding: 1.5em;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tcolor: var(--alternate-color);\n\tbackground-color: var(--alternate-bg-color);\n\tfont-family: Urbanist-Italic;\n\tborder: 1px solid var(--alternate-color);\n\tborder-radius: 5%;\n}\n\n.article {\n\tpadding: 1.5em;\n\ttext-align: center;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tcolor: var(--alternate-color);\n\tbackground-color: var(--alternate-bg-color);\n\tfont-family: Urbanist-Italic;\n\tborder: 1px solid var(--alternate-color);\n\tborder-radius: 5%;\n}\n\n.title {\n\tfont-family: "Urbanist-Black", "Lemon/Milk", "Myriad Pro", helvetica, sans-serif;\n\tfont-size: 2em;\n\tline-height: 1.5em;\n\ttext-align: center;\n\ttext-decoration: underline;\n}\n\n.section-title {\n\tfont-family: "Urbanist-Black", "Lemon/Milk", "Myriad Pro", helvetica, sans-serif;\n\tfont-size: 2em;\n\tline-height: 1.5em;\n\ttext-align: center;\n}\n\n.sig {\n\tfont-family: "White Modesty";\n\tfont-size: 4em;\n\tline-height: 1.5em;\n\ttext-align: center;\n}\n\n/* Table Div */\n.tables table {\n\tmargin-bottom: 0px;\n\tmargin-top: 0px;\n}\n\n.tables table:last-child {\n\tmargin-bottom: 50px;\n}\n\n.tables table:first-child {\n\tmargin-top: 50px;\n}\n\n.footer {\n\tposition: fixed;\n\tleft: 0;\n\tbottom: 0;\n\twidth: 100%;\n\tbackground-color: var(--main-bg-color);\n\tcolor: var(--main-color);\n\ttext-align: center;\n}\n\n.vertical-center {\n\tmargin: 0;\n\tposition: absolute;\n\ttop: 50%;\n\ttransform: translateY(-50%);\n\t-ms-transform: translateY(-50%);\n}\n\n.center {\n\tdisplay: table;\n\twidth: auto;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\n.center td {\n\ttext-align: center;\n}\n\n.center50 {\n\tdisplay: table;\n\twidth: 50%;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\n.center50 td {\n\ttext-align: center;\n}\n\n.center70 {\n\tdisplay: table;\n\twidth: 70%;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\n.center70 td {\n\ttext-align: center;\n}\n\n.note {\n\tfont-family:\n\t\t"Urbanist-Thin",\n\t\t-apple-system,\n\t\tBlinkMacSystemFont,\n\t\t"helvetica neue",\n\t\thelvetica,\n\t\troboto,\n\t\tnoto,\n\t\t"segoe ui",\n\t\tarial,\n\t\tsans-serif;\n\tfont-size: .8em;\n\ttext-align: center;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\nblockquote {\n\tfont-style: italic;\n\tmargin: 4em 2em;\n\tpadding: 1em;\n\ttext-align: center;\n\tbackground-color: var(--alternate-bg-color);\n\tcolor: var(--alternate-color);\n}\n\nhr {\n\tmargin: 5px;\n}\n\n#titlepage {\n\tcolor: var(--main-bg-color);\n}\n\np.title {\n\ttext-align: center;\n}\n\n/* Styles for cover.xhtml */\nbody.cover {\n\tmargin: 0;\n\tpadding: 0;\n\ttext-align: center;\n}\n\np.cover {\n\tmargin: 0;\n\tpadding: 0;\n\ttext-align: center;\n}\n\nimg.cover {\n\theight: 100%;\n\tmargin: 0;\n\tpadding: 0;\n}\n\nhtml.eob {\n\tmargin: 0;\n\tpadding: margin;\n\ttext-align: center;\n}\n\nbody.eob {\n\t/* margin-left: auto; */\n\t/* margin-right: auto; */\n\tpadding: 0;\n\t/* text-align: center; */\n\tbackground-color: var(--main-bg-color);\n}\n\nh2.eob {\n\tdisplay: block;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tpadding-top: 30px;\n\ttext-align: center;\n\tcolor: rgba(0, 0, 0, 0);\n}\n\nh3.eob {\n\tmargin-left: auto;\n\tmargin-right: auto;\n\tpadding: 0;\n\ttext-align: center;\n\tcolor: var(--main-color)\n}\n\npicture.eob {\n\tmargin: 0;\n\tpadding: 0;\n\ttext-align: center;\n}\n\nfigure.eob {\n\tdisplay: block;\n\tmargin-left: auto;\n\tmargin-right: auto;\n}\n\np.eob {\n\tmargin: 0;\n\tpadding-bottom: 40px;\n\ttext-align: center;\n\tcolor: rgba(0, 0, 0, 0);\n\tfont-family: "Urbanist-Thin", "Lemon/Milk", "Myriad Pro", helvetica, sans-serif;\n}\n\np.eob-thin {\n\tdisplay: block;\n\ttext-align: center;\n\tfont-family: Urbanist-Thin;\n\tmargin-left: 0;\n\tmargin-right: auto;\n}\n\nimg.eob {\n\twidth: 100%;\n\tmax-height: 200px;\n\tmargin: 0;\n\tpadding: 0;\n}\n\nh1.titlepage {\n\tmargin-left: auto;\n\tmargin-right: auto;\n\ttext-align: center;\n\tcolor: var(--main-color)\n}\n\nh3.titlepage {\n\tmargin-left: auto;\n\tmargin-right: auto;\n\ttext-align: center;\n\tcolor: var(--main-color)\n}\n\nfigure.titlepage-gem {\n\twidth: 120px;\n\theight: 60px;\n\tmargin-left: auto;\n\tmargin-right: auto;\n\ttext-align: center;\n}',
    },
    {
        "file": "LICENSE",
        "filepath": LICENSE_FILEPATH,
        "type": "text",
        "content": 'MIT License\n\nCopyright (c) 2022 Maxwell Owen Ludden\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.',
    },
    {
        "file": ".gitignore",
        "filepath": GITIGNORE_FILEPATH,
        "type": "text",
        "content": "# Byte-compiled / optimized / DLL files\n__pycache__/\n*.py[cod]\n*$py.class\n\n# C extensions\n*.so\n\n# Distribution / packaging\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\nshare/python-wheels/\n*.egg-info/\n.installed.cfg\n*.egg\nMANIFEST\n\n# PyInstaller\n#  Usually these files are written by a python script from a template\n#  before PyInstaller builds the exe, so as to inject date/other infos into it.\n*.manifest\n*.spec\n\n# Installer logs\npip-log.txt\npip-delete-this-directory.txt\n\n# Unit test / coverage reports\nhtmlcov/\n.tox/\n.nox/\n.coverage\n.coverage.*\n.cache\nnosetests.xml\ncoverage.xml\n*.cover\n*.py,cover\n.hypothesis/\n.pytest_cache/\ncover/\n\n# Translations\n*.mo\n*.pot\n\n# Django stuff:\n*.log\nlocal_settings.py\ndb.sqlite3\ndb.sqlite3-journal\n\n# Flask stuff:\ninstance/\n.webassets-cache\n\n# Scrapy stuff:\n.scrapy\n\n# Sphinx documentation\ndocs/_build/\n\n# PyBuilder\n.pybuilder/\ntarget/\n\n# Jupyter Notebook\n.ipynb_checkpoints\n\n# IPython\nprofile_default/\nipython_config.py\n\n# pyenv\n#   For a library or package, you might want to ignore these files since the code is\n#   intended to run in multiple environments; otherwise, check them in:\n# \.python-version\n\n# pipenv\n#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.\n#   However, in case of collaboration, if having platform-specific dependencies or dependencies\n#   having no cross-platform support, pipenv may install dependencies that don't work, or not\n#   install all needed dependencies.\n#Pipfile.lock\n\n# poetry\n#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.\n#   This is especially recommended for binary packages to ensure reproducibility, and is more\n#   commonly ignored for libraries.\n#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control\n#poetry.lock\n\n# pdm\n#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.\n#pdm.lock\n#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it\n#   in version control.\n#   https://pdm.fming.dev/#use-with-ide\n.pdm.toml\n\n# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm\n__pypackages__/\n\n# Celery stuff\ncelerybeat-schedule\ncelerybeat.pid\n\n# SageMath parsed files\n*.sage.py\n\n# Environments\n.env\n.venv\nenv/\nvenv/\nENV/\nenv.bak/\nvenv.bak/\n\n# Spyder project settings\n.spyderproject\n.spyproject\n\n# Rope project settings\n.ropeproject\n\n# mkdocs documentation\n/site\n\n# mypy\n.mypy_cache/\n.dmypy.json\ndmypy.json\n\n# Pyre type checker\n.pyre/\n\n# pytype static type analyzer\n.pytype/\n\n# Cython debug symbols\ncython_debug/\n\n# PyCharm\n#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can\n#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore\n#  and can be added to the global gitignore or merged into this file.  For a more nuclear\n#  option (not recommended) you can uncomment the following to ignore the entire idea folder.\n#\.idea/\n",
    },
    {
        "file": ".env",
        "filepath": f"{BASE}/.env",
        "type": "text",
        "content": "# Pushover API\nAPI_TOKEN='op://1Password/pushover/API/token'\nUSER_KEY ='op://1Password/Pushover/api/userkey'\n\n## Notion API\nNOTION_API='op://1Password/notion/api/token'\nNOTION_DB_CHAPTER='op://1Password/Notion/database/chapter'\n\n# MongoDb Atlas (private)- DB: Supergene\n\n## MongoDB Connection String\nSUPERGENE='op://1Password/mongodb/atlas/supergene'\nLOCALDB='op://1Password/mongodb/atlas/localdb'\n\n## Data API\nDATA_API_KEY='op://1Password/mongodb/dataapi/key'\nDATA_API_TOKEN='op://1Password/mongodb/dataapi/token'\nfindOne='op://1Password/mongodb/dataapi/findOne'\nupdateOne='op://1Password/mongodb/dataapi/updateOne'\nfind='op://1Password/mongodb/dataapi/find'\ninsertOne='op://1Password/mongodb/dataapi/insertOne'\ninsertMany='op://1Password/mongodb/dataapi/insertMany'\nupdateMany='op://1Password/mongodb/dataapi/updateMany'\nreplaceOne='op://1Password/mongodb/dataapi/replaceOne'\ndeleteOne='op://1Password/mongodb/dataapi/deleteOne'\ndeleteMany='op://1Password/mongodb/dataapi/deleteMany'\naggregate='op://1Password/mongodb/dataapi/aggregate'",
    },
]


def test_css():
    """test printing css from setup_files.py"""
    for file in FILES:
        if file["file"] == "style.css":
            content = file["content"]
            filepath = file["filepath"]
            with open(filepath, "w") as outfile:
                outfile.write(content)


def created_dir_panel(dirname: str, dirpath: str) -> Panel:
    """
    Creates a panel for the directory that was created.

    Args:
        dirname (str): The name of the directory that was created.
        dirpath (str): The path to the directory that was created.

    Returns:
        Panel: A panel for the directory that was created.
    """
    return Panel(
        f"[value]Created [/][italic purple]{dirname}[/][value] at [/][light_grey]{dirpath}[/]",
        title="[purple]Created Directory[purple]",
        title_align="center",
        border_style=Style(color="#3a0085", bold=True),
        expand=True,
        width=120,
        padding=(0, 1, 0, 1),
    )


def created_file_panel(filename: str, filepath: str) -> Panel:
    """
    Creates a panel for the file that was created.

    Args:
        filename (str): The name of the file that was created.
        filepath (str): The path to the file that was created.

    Returns:
        Panel: A panel for the file that was created.
    """
    return Panel(
        f"[value]Created [/][italic green]{filename}[/][value] at [/][light_grey]{filepath}[/]",
        title="[green]Created File[green]",
        title_align="center",
        border_style=Style(color="#00b612", bold=True),
        expand=True,
        width=120,
        padding=(0, 1, 0, 1),
    )


def get_fonts():
    copy = Command("cp")
    master = "/Users/maxludden/dev/custom/fonts"
    with progress:
        write_fonts = progress.add_task(
            description="Copying Fonts...", total=len(FONTS)
        )
        for font in FONTS:
            copy(f"{master}/{font}", f"{BASE}/fonts")
            progress.update(write_fonts, advance=1, description=f"Copying {font}.")
            console.print(created_file_panel(font, f"{BASE}/fonts/{font}"))
    for font in FONTS:
        copy(f"{master}/{font}", f"{BASE}/static/{font}")
        console.print(created_file_panel(font, f"{BASE}/static/{font}"))


def get_dotenv():
    """Get the dotenv file from the user's home directory."""
    copy = Command("cp")
    copy("/Users/maxludden/custom/.env", f"{BASE}/.env")
    console.print(created_file_panel(".env", f"{BASE}/.env"))


def make_files() -> None:
    """Creates the necessary files for logging."""
    # Create directories
    for directory in DIRS:
        if not directory.exists():
            directory.mkdir()
    with progress:
        write_files = progress.add_task(
            description="Creating Files...", total=len(FILES)
        )
        for file in FILES:
            path = Path(file["filepath"])
            if not path.exists():
                name = file["file"]
                file_type = file["type"]
                content = file["content"]
                with open(path, "w") as outfile:
                    outfile.write(content)
                # console.print(created_file_panel(name, file["filepath"]))
                filename = file["file"]
                progress.update(
                    write_files, advance=1, description=f"Created {filename}."
                )

            else:
                filename = file["file"]
                progress.update(
                    write_files,
                    advance=1,
                    description=f"Skipped {filename} as it already existed.",
                )

    get_fonts()


def show_files() -> None:
    """
    Shows the files that were created.
    """
    num_of_files = 0
    table = Table(
        show_header=False,
        header_style="bold magenta",
        row_styles=["#a600ff", "#fb7aff"],
        show_lines=True,
        style="#ffa9eb",
    )
    table.add_column("#", style="dim", justify="right")
    table.add_column("File", justify="left")
    table.add_column("Filepath", justify="left")

    for x, file in enumerate(FILES, start=1):
        name = file["file"]
        path = file["filepath"]
        # console.print(f"{name} -> {path}")
        num_of_files += 1
        table.add_row(f"{x}", name, str(path))

    console.print(table, justify="center")
