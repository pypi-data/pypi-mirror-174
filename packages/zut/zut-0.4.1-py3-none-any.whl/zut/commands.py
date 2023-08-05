"""
Add and execute commands easily, based on argparse.
Usefull for non-Django applications.
For Django applications, use including command management instead.
"""
from __future__ import annotations
import sys, argparse
from types import ModuleType
from typing import Callable
from pathlib import Path
from importlib import import_module
from importlib.util import find_spec
from .colors import FOREGROUND_RED

def add_module_command(subparsers: argparse._SubParsersAction, module: str|ModuleType, name: str = None):
    """
    Add command from functions in a module. By default, command function is expected to be named "handler"
    and arguments definition function is expected to be named "add_arguments".
    """
    if not isinstance(module, ModuleType):
        module = import_module(module)
    if not name:
        name = module.__name__.split(".")[-1]

    handle = getattr(module, "handle")
    add_arguments = getattr(module, "add_arguments", None)
    help = getattr(module, "HELP", None)

    subparser = subparsers.add_parser(name, help=help, description=help) # help: in list of commands, description: in command help
    subparser.set_defaults(func=handle)
    if add_arguments:
        add_arguments(subparser)


def add_packages_commands(subparsers: argparse._SubParsersAction, package: str):
    package_spec = find_spec(package)
    if not package_spec:
        raise KeyError(f"package not found: {package}")
    if not package_spec.origin:
        raise KeyError(f"not a package: {package} (did you forget __init__.py ?)")
    package_path = Path(package_spec.origin).parent
    
    for module_path in package_path.iterdir():
        if module_path.is_dir() or module_path.name.startswith("_") or not module_path.name.endswith(".py"):
            continue

        module = module_path.stem
        add_module_command(subparsers, f"{package}.{module}")


def add_object_commands(subparsers: argparse._SubParsersAction, instance: any, exclude = []):
    for name in dir(instance):
        if exclude and name in exclude:
            continue

        if name.startswith("_") or name.endswith("_arguments"):
            continue

        func = getattr(instance, name)
        if not callable(func):
            continue

        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=func)

        add_arguments_func = getattr(instance, f"{name}_add_arguments", None)
        if add_arguments_func:
            add_arguments_func(subparser)


def exec_command(parser: argparse.ArgumentParser, default_func: Callable = None):
    args = vars(parser.parse_args())
    func = args.pop("func", None)
    if not func:
        if default_func:
            func = default_func
        else:
            print(FOREGROUND_RED % "missing command name")
            sys.exit(2)

    r = func(**args)
    if not isinstance(r, int):
        r = 0 if r is None or r is True else 1
    sys.exit(r)


def call_command(cmd: str, *args: any, parser: argparse.ArgumentParser = None):
    if parser is None:
        from __main__ import parser

    cmd_with_args = [cmd] + [str(arg) for arg in args]
    args = vars(parser.parse_args(cmd_with_args))

    func = args.pop("func", None)
    if not func:
        raise ValueError("missing command name")

    return func(**args)
