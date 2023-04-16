#!/usr/bin/env python
import json
import os
from os import getenv

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

def add_satgpt_prompt():
    file_path = getenv("HOME") + "/.config/shell_gpt/roles/satgpt.json"
    # copy from ./.config/satgpt.json to file_path if it doesn't exist already
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump({}, f)

# https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        add_satgpt_prompt()
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        add_satgpt_prompt()
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

if __name__ == "__main__":
    # setup for satgpt
    setup(
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
    )