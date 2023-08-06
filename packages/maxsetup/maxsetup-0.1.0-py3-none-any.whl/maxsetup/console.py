# /maxsetup/console.py

from turtle import bgcolor
from typing import Optional, List
from inspect import getframeinfo, currentframe

from rich.text import Text
from rich.color import Color
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.repr import Result, rich_repr
from rich.table import Column
from rich.theme import Theme
from rich.traceback import install as install_rich_traceback


__version__ = "0.1.0"


""" This script is used to generate a rich console with a custom theme. In addition to the console, it also generates a Customized Rich Progress Bar."""

__all__ = [
    "theme_dict",
    "theme",
    "text_column",
    "spinner_column",
    "bar_column",
    "mofn_column",
    "time_elapsed_column",
    "time_remaining_column",
    "MaxConsole",
    "console",
    "progress",
    "magenta",
    "purple",
    "blue_violet",
    "cyan",
    "cornflower_blue",
    "blue",
    "green",
    "yellow",
    "orange",
    "red",
    "white",
    "light_grey",
    "grey",
    "dark_grey",
    "black",
    "validate_console",
    "validate_progress",
]

# . Hex Colors
magenta = "#ff00ff"  #               #ff00ff
purple = "#af00ff"  #                #af00ff
blue_violet = "#5f00ff"  #           #5f00ff
blue = "#0000ff"  #                  #0000ff
cornflower_blue = "#249df1"  #       #249df1
cyan = "#00ffff"  #                  #00ffff
green = "#00ff00"  #                 #00ff00
yellow = "#ffff00"  #                #ffff00
orange = "#ff8800"  #                #ff8800
red = "#ff0000"  #                   #ff0000

# . Hex Tints
white = "#ffffff"  #                  #ffffff
light_grey = "#e2e2e2"  #            #e2e2e2
grey = "#808080"  #                  #808080
dark_grey = "#2e2e2e"  #             #2e2e2e
black = "#000000"  #                 #000000


theme_dict = {
    "magenta": "#ff00ff",  #         #ff00ff
    "purple": "#af00ff",  # P        #af00ff
    "blue_violet": "#5f00ff",  #     #5f00ff
    "blue": "bold #0000FF",  #       #0000ff
    "cornflower_blue": "#249df1",  # #249df1
    "cyan": "#00ffff",  #            #00ffff
    "green": "#00ff00",  #           #00ff00
    "yellow": "#ffff00",  #          #ffff00
    "orange": "#ff8800",  #          #ff8800
    "red": "#ff0000",  #             #ff0000
    "white": "#ffffff",  #           #ffffff
    "light_grey": "#e2e2e2",  #      #e2e2e2
    "grey": "#808080",  #            #808080
    "dark_grey": "#2e2e2e",  #       #2e2e2e
    "black": "#000000",  #           #000000
    "debug": "bold bright_cyan",  #    #00ffff
    "info": "bold cornflower_blue",  # #249df1
    "success": "bold bright_green",  # #00ff00
    "warning": "bold bright_yellow",  ##ffff00
    "error": "bold orange1",  #        #ff8800
    "critical": "bold reverse red",  # #ff0000
    "value": "bold bright_white",  #   #ffffff
    "title": "bold purple",  #         #af00ff
    "key": "italic magenta",  #        #ff00ff
    "lines": "blue_violet",  #         #5f00ff
}
theme = Theme(theme_dict)

# Column for the custom progress bar
text_column = TextColumn("[progress.description]{task.description}")
spinner_column = SpinnerColumn(
    spinner_name="point",
    style="yellow",
    finished_text=Text("✓", style="green"),
    table_column=Column(),
)
bar_column = BarColumn(
    bar_width=None,  # Full width progress bar
    style=Style(color="cornflower_blue", bgcolor="cornflower_blue"),  # While in-progress
    complete_style=Style(color="green", bgcolor="green"),  # Done
    finished_style=Style(color="green", bgcolor="#333333"),  # After completion
    table_column=Column(ratio=3),
)
mofn_column = MofNCompleteColumn()
time_elapsed_column = TimeElapsedColumn()
time_remaining_column = TimeRemainingColumn()


class MaxConsole(Console):
    """Generate a custom themed Rich Console."""

    theme: Theme = theme
    console: Console = Console(theme=theme)
    progress: Progress = Progress(
        text_column,
        spinner_column,
        bar_column,
        mofn_column,
        time_elapsed_column,
        time_remaining_column,
        console=console,
    )

    def __init__(self, theme: Theme = Theme(theme_dict)) -> None:
        # Custom Theme
        self.theme = theme

        # Custom Console
        console = Console(theme=theme, color_system="truecolor", tab_size=4)
        install_rich_traceback(console=console, show_locals=True)
        self.console = console

        # Custom Progress Bar
        self.progress = Progress(
            text_column,
            spinner_column,
            bar_column,
            mofn_column,
            time_elapsed_column,
            time_remaining_column,
            console=console,
        )


console = MaxConsole().console
progress = MaxConsole().progress


def validate_console(console: Optional[Console] = console) -> Console:
    """
    Validate the console provided. If it is None, initialize a new console.

    Args:
        console (Optional[Console]): The console to validate.

    Returns:
        console (`rich.console.Console`): The validated console.
    """
    if not console:
        console = MaxConsole().console

        # Logging
        frameinfo = getframeinfo(currentframe())  # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.log(
            Panel(
                f"[value]No console provided. Initializing a new console.",
                title=f"[title]Console Validation[/]",
                title_align="left",
                border_style="warning",
                expand=True,
                width=80,
                subtitle=f"[key]maxsetup[/][white] | [/][warning] line{current_lineno}[/]",
                subtitle_align="right",
            ),
            justify="center",
        )
        return console

    else:
        console = console
        return console


def validate_progress(progress: Progress = progress) -> Progress:
    """Validate the progress bar provided. If it is None, initialize a new progress bar."""

    if not progress:
        progress = MaxConsole().progress

        frameinfo = getframeinfo(currentframe())  # type: ignore
        current_lineno = int(frameinfo.lineno) + 2
        console.log(
            Panel(
                f"[value]No progress bar provided. Initializing a new progress bar.",
                title=f"[title]Progress Bar Validation[/]",
                title_align="left",
                border_style="warning",
                expand=True,
                width=80,
                subtitle=f"[key]maxsetup[/][white] | [/][warning] line{current_lineno}[/]",
                subtitle_align="right",
            ),
            justify="center",
        )
        return progress
    else:
        progress = progress
        return progress


progress = validate_progress()
