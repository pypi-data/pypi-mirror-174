"""Main module"""
import sys
import importlib
from pathlib import Path
import argparse
import os
import re
from typing import List

import yaml
from yaml.loader import SafeLoader
from colorama import init, Fore


def init_parser() -> argparse.ArgumentParser:
    """Initialize argument parser.

    returns:
        - ArgumentParser with configured arguments.
    """
    parser = argparse.ArgumentParser(
        prog="Boost", description="A modern python multiplatform build system"
    )
    parser.add_argument(
        "boost", help="Boost operation", nargs="?", default="", type=str
    )
    return parser


def validate_boost() -> dict:
    """Reads and validates boost.yaml file.

    returns:
        - dict containing parsed and validated yaml.
        - bool as false in case yaml file could not be readen or validated.
    """
    if not BOOST_FILE.exists():
        return {
            "error": "Boost file does not exist, please read https://github.com/dloez/boost/tree/main#using-boost"
        }

    with open(BOOST_FILE, "r", encoding="utf8") as handler:
        boost_data = yaml.load(handler, Loader=SafeLoader)
    if "boost" in boost_data:
        return boost_data
    return {
        "error": "boost section file does not exist, please read https://github.com/dloez/boost/tree/main#using-boost"
    }


def call_command(cmd: str, args: List[str]) -> dict:
    """Execute given command.

    Given command is dyanmically imported from cmd module.
    If module is not found, we will be opnening a shell an executing the command
    directly.

    params:
        - cmd: command that needs to be executed.
        - args: command arguments.

    returns:
        - dict containing executed command output on output key or error on error key.
    """
    try:
        command = importlib.import_module(f"boostbuild.cmd.{cmd}")
    except ModuleNotFoundError:
        # In case the command does not exist on Boost ecosystem, call unkown command.
        # unkown command does also need to know required command, this is why we are
        # adding cmd to args at 0 index.
        command = importlib.import_module("boostbuild.cmd.unkown")
        args.insert(0, cmd)

    # validate if command has implement a generic execution
    if hasattr(command, "generic_exec"):
        return command.generic_exec(args)

    # command has different behaviour for windows/posix
    os_to_function = {"nt": "win_exec", "posix": "posix_exec"}
    try:
        call = os_to_function[os.name]
        return getattr(command, call)(args)
    except KeyError:
        return {"error": "unsuported OS"}


def get_storage(boost_data: dict, variables: List[str]) -> dict:
    """Store commands variables.

    From list of required variables, store on a dictionary each variable key and value.

    params:
        - boost_data: yaml parsed boost file.
        - variables: list of required variables to store.

    returns:
        - dict containing all stored variables for commands use or dict containing error key on case
        there was an error building the storage.
    """
    storage = {}
    for variable in variables:
        value = ""
        clean_var = variable.replace("{", "").replace("}", "")
        if clean_var in boost_data["vars"]:
            if boost_data["vars"][clean_var].startswith("exec "):
                cmd, *args = (
                    boost_data["vars"][clean_var].replace("exec ", "").split(" ")
                )
                cmd_output = call_command(cmd, args)
                if "error" in cmd_output:
                    return cmd_output
                else:
                    value = cmd_output["output"]
            else:
                value = boost_data["vars"][clean_var]
        else:
            try:
                value = os.environ[clean_var]
            except KeyError:
                return {
                    "error": f"variable {clean_var} is not declared neither on vars section or on system env variables"
                }
        storage[variable] = value
    return storage


def main() -> int:
    """Main function"""
    init(autoreset=True)

    parser = init_parser()
    args = parser.parse_args()

    boost_data = validate_boost()
    if "error" in boost_data:
        print(Fore.RED + boost_data["error"])
        return 1

    if not args.boost:
        # if not boost operation was specified, use first one
        boost = next(iter(boost_data["boost"]))
    else:
        boost = args.boost

    variables = re.findall("{.*}", boost_data["boost"][boost])
    commands = boost_data["boost"][boost].strip().split("\n")
    total_commands = len(commands)
    print(Fore.CYAN + f"Boosting {boost} - {total_commands} commands")

    storage = get_storage(boost_data, variables)
    if "error" in storage:
        print(Fore.RED + storage["error"])
        return 1

    for i, cmd in enumerate(commands):
        variables = re.findall("{.*}", cmd)
        for var in variables:
            cmd = cmd.replace(var, storage[var])
        print(Fore.GREEN + f"    - [{i + 1}/{total_commands}] - {cmd}")
        cmd, *args = cmd.split(" ")
        output = call_command(cmd, args)
        if "error" in output:
            print(Fore.RED + output["error"])
            return 1
    return 0


# TODO: Implement custom file parsing, yaml will not be enough for future functionalities.
# TODO: Better error handling.

BOOST_FILE = Path("boost.yaml")

if __name__ == "__main__":
    sys.exit(main())
