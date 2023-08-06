# maxsetup/myaml.py
from pathlib import Path
from typing import Any

import yaml
from rich import inspect, print

# Import UnsafeLoader
try:
    from yaml import CUnsafeLoader as Loader
except ImportError:
    from yaml import UnsafeLoader as Loader


# Import SafeLoader
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


# Import Dumper
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

# Import SafeDumper
try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper


"""
    This script is used to provides a simple interface to the pyaml library based on the standard `json` library.
"""

__all__ = ["load", "loads", "dump", "dumps"]

def load(filepath: str | Path) -> Any:
    """
    Load a yaml file.

    Args:
        filepath (str | Path): The path to the yaml file.

    Returns:
        Any: The loaded yaml file.
    """

    with open(filepath, "r") as infile:
        result = yaml.load(infile, Loader=Loader)
    return result


def loads(data: str) -> Any:
    """
    Load a yaml file.

    Args:
        data (str): The yaml data to load.

    Returns:
        Any: The loaded yaml file.
    """
    result = yaml.load(data, Loader=Loader)
    return result


def dump(data: Any, filepath: str | Path) -> None:
    """
    Serialize a yaml file using the normal pyaml library.

    Args:
        data (Any): The data to serialize.
        filepath (str | Path): The path to the yaml file.
    """
    data = yaml.dump(
        data, Dumper=Dumper, mode="wt", encoding="utf-8", indent=2
    )  # type: ignore
    inspect(data)
    with open(filepath, "w") as outfile:
        outfile.write(data)


def dumps(data: Any) -> str:
    """
    Serialize a yaml string form a python object.add()

    Args:
        data (Any): The data to serialize.

    Returns:
        str: The serialized yaml string.
    """
    data = yaml.dump(
        data, Dumper=Dumper, mode="wt", encoding="utf-8", indent=2
    )  # type: ignore
    inspect(data)
    return data
