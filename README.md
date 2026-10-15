# SatGPT

## Status (2026-10)

Alpha from April 2023. Ported to shell-gpt 1.x on 2026-10-15, but the `stacker` path has not been
tested since then (Landsat on AWS is requester-pays and needs AWS credentials). The successor is
[satgpt-app](https://github.com/lalligagger/satgpt-app), with a live demo at
https://kevinlalli.me/satgpt-app/.

GPT for satellite mission planning. In development. Get your API keys ready!

SatGPT heavily leverages Shell GPT, a command-line UI for OpenAI's completion API, 
and its custom role feature. For SatGPT to work, we need to replace the default shell role
using the instructions below.

## Installation

1. Clone this repo. Installing from source will be more straightforward than PyPi install at this stage.

2. From inside repo root, install from source.

```
python -m pip install -e . 
```

3. Write the `satgpt` role for `shell-gpt` 1.x. This creates
`~/.config/shell_gpt/roles/Shell Command Generator.json`, the role `sgpt --shell` uses, and backs up
any existing file to `Shell Command Generator.json.bak` first.

```
python src/satgpt/make_role.py            # write the role file
python src/satgpt/make_role.py --print    # only print the JSON, write nothing
```

## Usage

1. Start the REPL in shell mode.

```
sgpt --shell --repl temp
```

2. Request a STAC search using natural language

```
>>> find all landsat 8&9 imagery over washington, DC in April 2023
```

3. Request edits or additional steps

```
>>> pipe the results to stacterm cal
```

4. Try other things!

https://user-images.githubusercontent.com/11700267/233900142-55a38676-32ab-4c78-8226-b338b9b3b876.mov
