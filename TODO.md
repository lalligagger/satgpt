# TODO: breaking upgrades

Dependencies that cannot move to their latest versions without code or upstream changes, found while
publishing 0.0.5 (2026-10-16). Everything else floats at the floors in `pyproject.toml`; `constraints.txt`
is the exact set that passed the smoke test.

## satgpt (this package)

- [ ] **geogif 0.3 pins `numpy<2` and `Pillow<11`.** Caps the `gif` extra at Python 3.12 and pulls numpy 1.x
      into any venv that installs it. Options: a PR upstream to relax the pins (geogif is small and inactive
      since Jan 2025), or replace `geogif.dgif` in `stacker.to_gif` with a ~40-line Pillow + xarray GIF writer
      and drop the extra.
- [ ] **stacterm 0.1.0 pins `pandas~=1.2`.** No wheels for Python >= 3.12; conflicts with `stackstac>=0.5`
      (`pandas>=2`). It is only referenced in the role text ("pipe the results to stacterm cal"). Options: drop
      it from the role and the extra, or vendor a minimal calendar view over a pystac ItemCollection.
- [ ] **Earth Search v0 in the role text and the stacker example.** `earth-search.aws.element84.com/v0` was
      retired by Element84; v1 renamed collections (`sentinel-s2-l2a-cogs` -> `sentinel-2-l2a`) and asset keys.
      Update the example in `make_role.py` and re-test `stacker.promote_s3` (it rewrites `usgs-landsat-ard`
      hrefs) against v1 items.
- [ ] **Landsat is requester-pays.** `Stacker.to_gif` opens `s3://usgs-landsat/...` with `AWSSession(requester_pays=True)`,
      so it needs AWS credentials; document it, and fail with a clear message when they are missing.
- [ ] **shell-gpt 1.x REPL untested.** Role loading is verified (`sgpt --show-role`); `sgpt --shell --repl` with
      the custom role, and the model's output quality with current models, are not.
- [ ] **Python 3.13+ with the `gif` extra** is impossible until the geogif item above is done; `requires-python`
      stays `>=3.10` for the core package.

## satgpt-app (the web app, separate repo)

Kept on its 2023 pins (`requirements-2023-lock.txt`) on purpose; every item below is a rewrite, not a bump.

- [ ] **LangChain 0.0.240 -> 1.x.** `initialize_agent`, `AgentType.OPENAI_FUNCTIONS`, `ConversationBufferMemory`
      and `langchain.chat_models.ChatOpenAI` are gone; the agent loop in `app.py` is rewritten against
      `langchain-openai` tool calling, or LangChain is dropped for a direct OpenAI tool-calling loop (~60 lines).
- [ ] **openai 0.27 -> 1.x/2.x.** Client API changed completely; comes with the LangChain item.
- [ ] **Panel 1.1 `ChatBox` -> `ChatInterface`.** `pn.widgets.ChatBox` was removed in Panel 1.3; `app.py` and the
      `chat()` callback change shape. Bokeh 3.1 -> 3.9 follows Panel.
- [ ] **pandas 1.5 -> 2.x/3.x, numpy 1.23 -> 2.x.** `datashader`/`numba` and `odc-stac`/`xarray` versions move
      together; the index pipeline (`compute_index`, the quantile stretch) needs re-testing on real scenes.
- [ ] **spyndex 0.4 -> 0.12.** Drags in the Earth Engine client and `ee-extra`; consider vendoring the handful
      of index formulas the app exposes.
- [ ] **Intel Python 3.11 under Rosetta -> arm64 3.12+.** The Mac revival only works on the Intel build because
      of the 2023 pins; after the bumps above, an arm64 venv should be the default.
- [ ] **Landsat requester-pays** (same as above): `AWS_REQUEST_PAYER=requester` plus credentials, or Sentinel-2 only.
