# envdo

[![PyPI version](https://badge.fury.io/py/envdo.svg)](https://badge.fury.io/py/envdo)
[![Python version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Repo](https://img.shields.io/badge/repo-GitHub-black)](https://github.com/NewToolAI/envdo)

\[ [中文](README_zh.md) | English \]

Configure environment variables for Python code or command-line programs, providing dotenv management with group-based switching.

## Features

- **Group Environment Configuration** - Configure a set of environment variables for programs without affecting the system environment
- **Multi-Environment Management** - Support multiple environment configurations for quick switching
- **Sensitive Information Protection** - Automatically hide sensitive information (TOKEN, KEY, PASSWORD, etc.)
- **Interactive Selection** - Support interactive environment configuration selection
- **Clear Output** - Use the rich library for clear terminal output

## Installation

```bash
pip install envdo
```

```bash
pip install git+https://github.com/NewToolAI/envdo.git
```

## Configuration

Create a configuration file `.envdo.json` (in project directory) or `~/.envdo.json` (in user directory):

```json
{
    "deepseek-3.2": {
        "ANTHROPIC_MODEL": "deepseek-reasoner",
        "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "your-token-here"
    },
    "glm-4.7": {
        "ANTHROPIC_MODEL": "glm-4.7",
        "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "your-token-here"
    },
    "claude-opus": {
        "ANTHROPIC_MODEL": "claude-opus-4-5",
        "ANTHROPIC_BASE_URL": "https://api.anthropic.com",
        "ANTHROPIC_AUTH_TOKEN": "your-token-here",
        "HTTP_PROXY": "http://127.0.0.1:7890",
        "HTTPS_PROXY": "http://127.0.0.1:7890",
        "NO_PROXY": "localhost,127.0.0.1"
    }
}
```


## Programmatic Usage

```python
from envdo import load_envdo

load_envdo('example-1')
```

## Command Line Usage

![Demo 0](demo-0.png)

### List All Environment Configurations

```bash
envdo list
```

![Demo 1](demo-1.png)

### Interactive Environment Selection

```bash
envdo select <command>
```

![Demo 2](demo-2.png)

### Run Command with Specified Environment

```bash
envdo gpt-5.2 <command>
```

![Demo 3](demo-3.png)

### Other Commands

```bash
envdo -v          # Show version
envdo --version
envdo -h          # Show help
envdo --help
```

## Configuration Notes

- Configuration file priority: `.envdo.json` in current directory > `~/.envdo.json` in user directory
- On first run, if the configuration file does not exist, an example configuration file will be automatically created
- Sensitive information (containing keywords TOKEN, KEY, PASSWORD, SECRET, AUTH, CREDENTIAL, etc.) will be automatically displayed as `***`

## License

MIT License
