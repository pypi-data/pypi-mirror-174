from __future__ import annotations

import random
from pathlib import Path
from typing import Optional

import ujson as json
from loguru import logger as log
from maxsetup.colors import gradient_panel_demo


# from loguru import Logger
from maxsetup.console import MaxConsole, console, validate_console
from maxsetup.setup_files import make_files

"""
This script is used to provide a simple interface to the loguru library based on the standard `logging` library.

`maxsetup.log` contains the following:

Constants:
    BASE - The pathlib Path object for the base directory of the project.

Functions:
    new_run - Initialize a new run.
    log_init - Initialize the logger.

Classes:
    DirectoryNotFound(FilenotFoundError)
    RunDictionaryError(OSError)
"""


class DirectoryNotFound(FileNotFoundError):
    pass


class RunDictionaryError(OSError):
    pass


# Logging Folder and Filepaths important to logging
BASE = Path.cwd()
run_file = BASE / "logs" / "run.txt"
if not run_file.exists():
    make_files()

# . ─────────────────── Gradient Text ─────────────────────────────────


# . ─────────────────── Run ─────────────────────────────────
@log.catch
def _get_last_run() -> int:
    """Get the last run number from the run.txt file."""
    with open("logs/run.txt", "r") as infile:
        last_run = int(infile.read())
        # console.log(f"Last Run: {last_run}")
        return last_run


@log.catch
def _update_run(last_run: int, write: bool = True) -> int:
    """Update the run.txt file with the next run number."""
    run = last_run + 1
    if write:
        with open(run_file, "w") as outfile:
            outfile.write(str(run))
    return run


@log.catch
def new_run() -> int:
    """Get the next run number."""
    last_run = _get_last_run()
    run = _update_run(last_run)
    return run




# . ──────────────────── Log Sinks  ───────────────────────────────
BASE = Path.cwd()
VERBOSE_LOG = BASE / "logs" / "verbose.log"
LOG = BASE / "logs" / "log.log"

@log.catch
def log_init(existing_console: Optional[Console], current_run: int) -> Logger:  # type: ignore
    """
    Configure Loguru Logger Sinks for the module.

    Args:
        `existing_console` (Optional[Console]): An existing console object to use for logging. If None, a new console will be created.add()

    Returns:
        `log` (Logger): A configured Loguru Logger object.
    """
    console = validate_console(console=MaxConsole().console)

    sinks = log.configure(
        handlers=[
            # _. Debug
            # Loguru Logger
            dict(  # . debug.log
                sink=f"{VERBOSE_LOG}",
                level="DEBUG",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
                rotation="10 MB",
            ),
            # _, INFO
            # Loguru Logger
            dict(
                sink=f"{LOG}",
                level="INFO",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
                rotation="10 MB",
            ),
            # _, INFO
            # Rich Console Log
            dict(
                sink=(
                    lambda msg: console.log(
                        msg, markup=True, highlight=True, log_locals=False
                    )
                ),
                level="INFO",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
            #! ERROR
            # Rich Console Log
            dict(
                sink=(
                    lambda msg: console.log(
                        msg, markup=True, highlight=True, log_locals=True
                    )
                ),
                level="ERROR",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
        ],
        extra={"run": current_run},  # > Current Run
    )
    log.debug("Initialized Logger")

    return log
