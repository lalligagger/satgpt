#!/usr/bin/env python
"""Write the satgpt role file for shell-gpt 1.x.

shell-gpt >= 1.0 keeps roles in ``~/.config/shell_gpt/roles/<name>.json`` and
``sgpt --shell`` uses the role named exactly "Shell Command Generator". The
JSON keys must match ``SystemRole.__init__(name, role, variables=None)``.

Usage:
    python src/satgpt/make_role.py           # write (backs up an existing file to .bak)
    python src/satgpt/make_role.py --print   # only print the JSON, write nothing
"""
import argparse
import json
import os
import platform
import shutil
from os import getenv, pathsep
from os.path import basename, expanduser

ROLE_NAME = "Shell Command Generator"

# The role text. {shell} and {os} are filled in by shell-gpt from "variables"
# when the role is loaded. Do not add other curly braces here.
SATGPT_ROLE = """###
Provide only {shell} commands for {os} without any description.
If there is a lack of details, provide most logical solution.
Ensure the output is a valid shell command.
If multiple steps required try to combine them together.
____

Here are some particular CLI packages to recommend and their use cases:

stac-client
Important: when using stac-client DO NOT format bounding boxes like: --bbox 102.5,22.5,103.5,23.5
The correct format is: --bbox 102.5 22.5 103.5 23.5
Important: do not return a stac-client command without providing a URL. If the user does not specify, use https://landsatlook.usgs.gov/stac-server/
The canonical stac-client command is: stac-client search URL --bbox BBOX --datetime DT --query QUERY
An example is:
stac-client search https://landsatlook.usgs.gov/stac-server/  --bbox 102.5 22.5 103.5 23.5 --collections landsat-c2l2-sr --datetime 2022-09-01/2023-04-30 --query "eo:cloud_cover<20"
IMPORTANT: NO COMMAS IN BETWEEN NUMERIC BBOX VALUES. USE SPACES ONLY BETWEEN BBOX VALUES. NO EXCEPTIONS.


Stacker
Stacker is a basic cli tool that wraps stackstac and geogif.
The below example uses a saved stac search and saves an animation of monthly resampled RGB data to test.gif.

stac-client search https://earth-search.aws.element84.com/v0 --bbox -77.119759 38.791645 -76.909393 38.995548 --datetime 2022-06-01/2022-08-31 > ./data/save-items.json \\
&& python src/satgpt/stacker.py --path=data/save-items.json --resolution=20 --bounds_latlon=-77.131,38.979,-76.893,38.811 - to_gif --to=test.gif --resample=1M

Note the " - to_gif" syntax, where the single hyphen is used to indicate that the command is to be piped to the next command.
Important: Don't forget the space on either side of these separators. It has to be " - to_gif" not " -to_gif"
Important: stac items cannot be piped directly for now, an intermediate save file must be used and it's path passed to stacker using --path
The "to_gif" is the name of the function in the Stacker class that will be called, and its flags can be passed after the command
____
"""

# shell-gpt's own roles are stored with this prefix; it is how a chat session
# recognises that it is still using the same role (SystemRole.same_role).
ROLE_TEMPLATE = "You are {name}\n{role}"


def _os_name():
    # adapted from https://github.com/TheR1D/shell_gpt/blob/main/sgpt/role.py
    current_platform = platform.system()
    if current_platform == "Linux":
        from distro import name as distro_name

        return "Linux/" + distro_name(pretty=True)
    if current_platform == "Windows":
        return "Windows " + platform.release()
    if current_platform == "Darwin":
        return "Darwin/MacOS " + platform.mac_ver()[0]
    return current_platform


def _shell_name():
    if platform.system() in ("Windows", "nt"):
        is_powershell = len(getenv("PSModulePath", "").split(pathsep)) >= 3
        return "powershell.exe" if is_powershell else "cmd.exe"
    return basename(getenv("SHELL", "/bin/sh"))


def build_role_json():
    """The role as shell-gpt 1.x expects it: keys name, role, variables."""
    return {
        "name": ROLE_NAME,
        "role": ROLE_TEMPLATE.format(name=ROLE_NAME, role=SATGPT_ROLE),
        "variables": {"shell": _shell_name(), "os": _os_name()},
    }


def role_file_path():
    home = getenv("HOME") or expanduser("~")
    return os.path.join(home, ".config", "shell_gpt", "roles", ROLE_NAME + ".json")


def make_satgpt_role(print_only=False):
    text = json.dumps(build_role_json(), indent=4)
    if print_only:
        print(text)
        return None

    file_path = role_file_path()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.exists(file_path):
        backup_path = file_path + ".bak"
        shutil.copy2(file_path, backup_path)
        print("Backed up existing role to: " + backup_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote satgpt role to:        " + file_path)
    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Write the satgpt role for shell-gpt 1.x (used by `sgpt --shell`)."
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_only",
        help="only print the role JSON, do not write any file",
    )
    args = parser.parse_args()
    make_satgpt_role(print_only=args.print_only)
