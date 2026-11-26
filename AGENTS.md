# SberCode - AI Coding Assistant

## Project Overview
SberCode is an AI coding assistant that provides tools for file system operations, command execution, and web requests. It's designed to work as a development assistant with capabilities to read, write, edit files, run commands, and make HTTP requests.

## Project Structure

```
.
├── .git/                    # Git repository
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── .sc-history.jsonl       # Session history log
├── .venv/                  # Virtual environment
├── config_example.json     # Configuration template
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # User documentation
├── src/
│   └── sbercode/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── api.py          # API client implementation
│       ├── cert.py         # Certificate handling
│       ├── colors.py       # Terminal color utilities
│       ├── history.py      # Session history management
│       ├── main.py         # Main entry point
│       └── functions/      # Tool implementations
│           ├── __init__.py
│           ├── __pycache__/
│           ├── create_dir.py
│           ├── edit_file.py
│           ├── list_files.py
│           ├── read_file.py
│           ├── remove_dir.py
│           ├── remove_file.py
│           ├── run_command.py
│           ├── web_fetch.py
│           └── write_file.py
├── uv.lock                 # Lock file for uv package manager
└── AGENTS.md               # This file
```

## Core Components

### Entry Point
- **main.py**: Main application entry point, defines the `main()` function
- **api.py**: Handles API communication with GigaChat
- **history.py**: Manages conversation history and session logging

### Tool System
All tools are implemented in `src/sbercode/functions/` and follow a consistent pattern:

#### File Operations
- **read_file.py**: Read file contents
- **write_file.py**: Write new files (with overwrite protection)
- **edit_file.py**: Edit existing files (find and replace)
- **list_files.py**: List directory contents
- **create_dir.py**: Create directories
- **remove_file.py**: Delete files
- **remove_dir.py**: Delete directories

#### Execution Tools
- **run_command.py**: Execute shell commands
- **web_fetch.py**: Make HTTP requests

### Configuration
- **pyproject.toml**: Project metadata, dependencies, and build configuration
- **config_example.json**: Template for user configuration (API token and model)

## Dependencies
- `httpx[http2]>=0.28.1`: HTTP client with HTTP/2 support
- `markdownify>=1.2.4`: HTML to Markdown converter
- Python >=3.14

## Running the Project

### Development Mode
```bash
uv run sbercode
```

### Installation
```bash
uv tool install .
```

### Configuration
Copy `config_example.json` to `~/.config/sbercode/config.json` and add your API token:
```json
{
    "token": "YOUR_BASIC_AUTH_TOKEN",
    "model": "GigaChat-3-Ultra"
}
```

## Tool Usage Guidelines

### File Operations
- Always use `read_file` before editing to understand current content
- Use `write_file` with `overwrite: false` by default for safety
- Use `edit_file` for precise modifications (find and replace)
- Check file existence before operations when possible

### Command Execution
- Use `run_command` for shell operations
- Be cautious with destructive commands
- Set appropriate timeouts (default: 10 seconds)

### Web Requests
- Use `web_fetch` for HTTP operations
- Can convert response to markdown or show original html source code
- Automatically follows redirects

## Development Notes
- The project uses `uv` as the package manager and build backend
- All tools are registered and available to the LLM agent
- Session history is logged to `.sc-history.jsonl`
- Virtual environment is managed by `uv` in `.venv/`

## License
0BSD - Free to reuse and modify.

## API Integration
The assistant uses GigaChat-3-Ultra model with API authentication. Token and model configuration is read from `~/.config/sbercode/config.json`.
