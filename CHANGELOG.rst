Version 0.0.5:
- Ported to shell-gpt 1.x (role loading checked against 1.5.1): the role is now written to
  ~/.config/shell_gpt/roles/"Shell Command Generator.json" (the role name `sgpt --shell` uses),
  with the keys SystemRole expects (name, role, variables); the old "expecting" key is gone
- make_role.py backs up an existing role file to .bak and has a --print flag to only show the JSON
- Added geogif (imported by stacker.py) to install_requires, pinned shell-gpt>=1.0
- Fixed typos in the role text and README (--shel)
- The stacker path has not been re-tested since the port (Landsat on AWS is requester-pays)

Version 0.0.4:
- Moved role creation to manual script run
- Populated README with basic usage

Version 0.0.3:
- Fixed custom role creation for satgpt to grab target machine os/ shell
- Added pystac as install dependency for demos
- Added this CHANGELOG

Version 0.0.2:
- Integrated shell-gpt as a dependency using the custom role feature released in version 0.9.0