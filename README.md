# SberCode

**SberCode** is a very dumb AI coding assistant. It is like OpenCode, but funnier in every way. Unfortunately, GigaChat models are way too underperforming for any real coding tasks

### Features
- Reads, writes, edits files
- Runs commands
- Run this command? `echo I am not able to use terminal`
- `python -m pip install pip install pip install pip install pip install pip install...`

## Installation and running

### 1. Get an API key

Follow <https://developers.sber.ru/docs/ru/gigachat/quickstart/ind-create-project>. To register, you need a russian phone number - you don't have to be Sberbank's client. API key is free, and limits are quite sizeable (resets yearly)

After obtaining it, edit `~/.config/sbercode/config.json` and add your API key:
```json
{
    "token": "YOUR_BASIC_AUTH_TOKEN",
    "model": "GigaChat-3-Ultra"
}
```

### 2. Run

This project uses `uv` to manage dependencies. Simply run:
```
uv run sbercode
```

And you are ready

# License
```
# Copyright 2026 Neltharion01
# SPDX-License-Identifier: 0BSD
```

Feel free to reuse
