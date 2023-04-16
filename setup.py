#!/usr/bin/env python
import json
import os
from os import getenv

from setuptools import setup

import platform
from os import getenv, pathsep
from os.path import basename
import json
from distro import name as distro_name

# adapted from https://github.com/TheR1D/shell_gpt/blob/main/sgpt/role.py
def make_satgpt_role():
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

    ____
    """.format(shell=shell_name, os=os_name)

    satgpt_json ={
        "name": "satgpt", 
        "expecting": "Command", 
        "variables": {
            "shell": shell_name, 
            "os": os_name,
            }, 
            "role": SATGPT_ROLE
    }
    print(satgpt_json)
    file_path = getenv("HOME") + "/.config/shell_gpt/roles/satgpt.json"

    with open(file_path, "w") as f:
        f.write(json.dumps(satgpt_json, indent=4))


if __name__ == "__main__":
    # setup for satgpt
    make_satgpt_role()
    setup()