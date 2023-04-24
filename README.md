# SatGPT

GPT for satellite mission planning. In development. Get your API keys ready!

SatGPT heavily leverages Shell GPT, a command-line UI for OpenAI's completion API, 
and its features for custom role creation (as of 04/16/2023). Currently for SatGPT to work,
we need to overwrite the default shell roll using the instructions below.

## Installation

1. Clone this repo. Installing from source will be more straightforward than PyPi install at this stage.

2. From inside repo root, install from source.

```
python -m pip install -e . 
```

3. Overwrite `shell-gpt` default `shell` role with `satgpt` alpha demo.

```
python src/satgpt/make_role.py
```
## Usage

1. Start the REPL in shell mode.

```
sgpt --shel --repl temp
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
