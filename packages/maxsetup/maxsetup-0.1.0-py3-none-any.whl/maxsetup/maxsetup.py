from pathlib import Path
from typing import Optional
from rich import print, inspect
from rich.console import Group
from rich.style import Style
from rich.panel import Panel
from rich.table import Table, Column
from rich.layout import Layout, LayoutRender
from inspect import currentframe, getframeinfo


from maxsetup.colors import (
    ANSI_COLORS,
    ANSI_REGEX,
    COLOR_REGEX,
    COLORS_ANSI,
    HEX_REGEX,
    RGB_REGEX,
    ColorType,
    get_color_type,
    gradient,
    gradient_panel,
    hex_to_rgb,
    rainbow,
    rgb_to_hex,
    valid_ansi,
    valid_hex,
)
from maxsetup.console import (
    console,
    progress,
    validate_console,
    validate_progress,
)
from maxsetup.log import log, log_init, new_run

from maxsetup.myaml import load, loads, dump, dumps

# Initialize Console and Progress Bar
console = validate_console(console)
progress = validate_progress(progress)

# Initialize Logger
current_run = new_run()
gradient_run = gradient(f"{current_run}",3, "center")
log = log_init(console, current_run)

# Clear Console and Print Header
console.clear()
console.rule(title = gradient_run, style = "bold bright_white", align = 'center')
