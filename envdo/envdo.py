import sys
import subprocess
from pathlib import Path

from envdo import utils


VERSION = '0.1.0'

EXAMPLE_CONFIG = '''
{
    "example": {
        "ANTHROPIC_MODEL": "deepseek-reasoner",
        "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "xxx"
    }
}
'''


def run_command(argv: list):
    if len(argv) <= 2:
        utils.print_error(f'Please specify a command to run (e.g., envdo {sys.argv[1]} echo "Hello, World!")')
        sys.exit(1) 

    result = subprocess.run(argv[2:])
    return result.returncode


def run_envdo(config_path):
    if len(sys.argv) <= 1:
        utils.print_help()
        sys.exit(1)

    try: 
        config = utils.load_config(config_path)
    except Exception as e:
        utils.print_error(f'Error loading config. Please check the file format. Path: {config_path}')
        sys.exit(1)

    if sys.argv[1] in ('-v', '--version'):
        print(VERSION)
        sys.exit(0)

    elif sys.argv[1] in ('l', 'ls', 'list'):
        utils.list_env(config)
        sys.exit(0)

    elif sys.argv[1] in ('s', 'select', 'i', 'interactive'):
        config = utils.load_config(config_path)
        utils.select_env(config)

    elif sys.argv[1] in config.keys():
        utils.set_env(sys.argv[1], config)

    elif sys.argv[1] in ('h', 'help', '-h', '--help'):
        utils.print_help()
        sys.exit(0)

    else:
        utils.print_error(f'Unknown configuration: {sys.argv[1]}. Available: {", ".join(config.keys())}')
        sys.exit(1)


def run():
    config_path = Path('./.envdo.json')

    if not config_path.exists():
        config_path = Path('~/.envdo.json').expanduser()

        if not config_path.exists():
            config_path.write_text(EXAMPLE_CONFIG.strip())
    
    run_envdo(config_path)
    return_code = run_command(sys.argv)
    sys.exit(return_code)


def main():
    try:
        run()
    except Exception as e:
        utils.print_error(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
