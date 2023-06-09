#!/usr/bin/env python
import json
import os
import platform
from os import getenv, pathsep
from os.path import basename


# adapted from https://github.com/TheR1D/shell_gpt/blob/main/sgpt/role.py
def make_satgpt_role():
    from distro import name as distro_name

    operating_systems = {
        "Linux": "Linux/" + distro_name(pretty=True),
        "Windows": "Windows " + platform.release(),
        "Darwin": "Darwin/MacOS " + platform.mac_ver()[0],
    }
    current_platform = platform.system()

    os_name = operating_systems.get(current_platform, current_platform)
    if current_platform in ("Windows", "nt"):
        is_powershell = len(getenv("PSModulePath", "").split(pathsep)) >= 3
        shell_name = "powershell.exe" if is_powershell else "cmd.exe"
    else:
        shell_name = basename(getenv("SHELL", "/bin/sh"))

    SATGPT_ROLE = """###
    Provide only {shell} commands for {os} without any description.
    If there is a lack of details, provide most logical solution.
    Ensure the output is a valid shell command.
    If multiple steps required try to combine them together.
    ____

    Here are some particular CLI packages to reccomend and their use cases:

    stac-client
    Important: when using stac-client DO NOT format bounding boxes like: --bbox 102.5,22.5,103.5,23.5
    The correct format is: --bbox 102.5 22.5 103.5 23.5
    Important: do not return a stac-client command without providing a URL. If the user does not specify, use https://landsatlook.usgs.gov/stac-server/
    The cannonical stac-client command is: stac-client search URL --bbox BBOX --datetime DT --query QUERY
    An example is:
    stac-client search https://landsatlook.usgs.gov/stac-server/  --bbox 102.5 22.5 103.5 23.5 --collections landsat-c2l2-sr --datetime 2022-09-01/2023-04-30 --query "eo:cloud_cover<20"
    IMPORTANT: NO COMMAS IN BETWEEN NUMERIC BBOX VALUES. USE SPACES ONLY BETWEEN BBOX VALUES. NO EXECPTIONS.


    Stacker
    Stacker is a basic cli tool that wraps stackstac and geogif.
    The below example uses a saved stac search and saves an animation of monthly resampled RGB data to test.gif.

    stac-client search https://earth-search.aws.element84.com/v0 --bbox -77.119759 38.791645 -76.909393 38.995548 --datetime 2022-06-01/2022-08-31 > ./data/save-items.json \
    && python src/satgpt/stacker.py --path=data/save-items.json --resolution=20 --bounds_latlon=-77.131,38.979,-76.893,38.811 - to_gif --to=test.gif --resample=1M

    Note the " - to_gif" syntax, where the single hyphen is used to indicate that the command is to be piped to the next command. 
    Important: Don't forget the space on either side of these separators. It has to be " - to_gif" not " -to_gif"
    Important: stac items cannot be piped directly for now, an intermediate save file must be used and it's path passed to stacker using --path
    The "to_gif" is the name of the function in the Stacker class that will be called, and its flags can be passed after the command
    ____
    """.format(
        shell=shell_name, os=os_name
    )

    satgpt_json = {
        "name": "shell",
        "expecting": "Command",
        "variables": {
            "shell": shell_name,
            "os": os_name,
        },
        "role": SATGPT_ROLE,
    }

    file_path = getenv("HOME") + "/.config/shell_gpt/roles/shell.json"

    # make directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(json.dumps(satgpt_json, indent=4))


if __name__ == "__main__":
    # setup for satgpt
    make_satgpt_role()
