# Publishing satgpt to PyPI

A dry run for the racinglines release. What the 0.0.5 release needed, in order.

## Build and check (any machine)

```bash
python3 -m venv .venv-pkg && .venv-pkg/bin/pip install build twine
.venv-pkg/bin/python -m build          # dist/satgpt-X.Y.Z.tar.gz and -py3-none-any.whl
.venv-pkg/bin/twine check dist/*       # README renders, metadata valid
```

Then install the wheel into a fresh venv and run the console script before uploading:

```bash
python3 -m venv /tmp/t && /tmp/t/bin/pip install dist/*.whl && /tmp/t/bin/satgpt-role --print | head -3
```

## Upload

Two ways. The second is the one to keep.

1. **By hand, with an API token** (pypi.org -> Account settings -> API tokens, scope it to the project):
   ```bash
   read -rs 'TWINE_PASSWORD?PyPI token (pypi-...): '; export TWINE_PASSWORD TWINE_USERNAME=__token__
   .venv-pkg/bin/twine upload dist/*
   ```
2. **Trusted publishing from GitHub Actions** (`.github/workflows/publish.yml`): on pypi.org, project ->
   Settings -> Publishing -> add GitHub as a publisher (owner `lalligagger`, repo `satgpt`, workflow
   `publish.yml`, environment `pypi`). Then a tag releases:
   ```bash
   git tag v0.0.5 && git push origin v0.0.5
   ```
   The workflow builds, runs `twine check`, refuses a tag that does not match `src/satgpt/version.py`, and
   uploads with OIDC. No token stored anywhere.

## What we hit on the way (keep for racinglines)

- **Markdown README with no content type.** The 2023 `setup.cfg` had `long_description = file: README.md,
  CHANGELOG.rst` and no `long_description_content_type`; PyPI would have rendered it as broken reST. PEP 621
  `readme = "README.md"` sets the type from the extension.
- **No LICENSE file.** Metadata said nothing about a license. `license = "MIT"` (SPDX, setuptools >= 77) plus
  `license-files = ["LICENSE"]` puts the text in the wheel and the expression in the metadata.
- **Dead author email.** `kevin@opticsinspace.com` no longer exists; PyPI shows it on the project page.
- **Dynamic version from a module.** `version = { attr = "satgpt.version.__version__" }` works with the src
  layout as long as `version.py` has no imports; the publish workflow checks the git tag against it.
- **Missing dependencies.** `stacker.py` imported `geogif` and shell-gpt needs `click`, neither declared. A
  fresh-venv install of the wheel is the only test that catches this; `pip install -e .` in a dev venv does not.
- **Platform-only dependency.** `distro` is Linux-only: `"distro; sys_platform == 'linux'"`.
- **setup.py / setup.cfg removed.** One source of metadata; setuptools still writes a tiny `setup.cfg` into
  the sdist by itself, which is normal.
- **Changelog not in the sdist.** `MANIFEST.in` with `include CHANGELOG.rst`; `prune reference` keeps the
  sample STAC JSON out.
- **The package name was taken by its own 0.0.4.** You can only upload a new version, never replace one, and
  a yanked or deleted version number can never be reused. `racinglines` is free on PyPI as of 2026-10-16.
- **A dependency with a stale pin breaks the whole install.** `stacterm` 0.1.0 pins `pandas~=1.2` (no wheels
  past Python 3.11, and it conflicts with `stackstac>=0.5`), so pip backtracked into source builds that failed
  on CI and on the Mac. `geogif` pins `numpy<2`, which caps Python at 3.12. Both are now optional extras.
  Before a release, run `pip install dist/*.whl` in a fresh venv on every Python you claim, and read the
  `Collecting X (from Y)` lines when it goes wrong.
- **Your Python floor is your dependencies' floor.** rasterio 1.5 requires Python >= 3.12, so floors at today's
  versions mean `requires-python = ">=3.12"`; a 3.10 smoke job failed within seconds and told us. Test the
  install on every Python you claim, in CI, before tagging.
- **Heavy dependencies.** rasterio, dask and stackstac make a fresh install slow and version-sensitive.
