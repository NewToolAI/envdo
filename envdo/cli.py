import sys
import subprocess
from pathlib import Path

from envdo import utils


VERSION = '0.1.1'

EXAMPLE_CONFIG = '''
{
    "example-1": {
        "ANTHROPIC_MODEL": "deepseek-reasoner",
        "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "xxx"
    },
    "example-2": {
        "ENV_VAR": "xxx",
    }
}
'''


def run_command():
    if len(sys.argv) <= 2:
        utils.print_error(f'Please specify a command to run (e.g., envdo {sys.argv[1]} echo "Hello, World!")')
        sys.exit(1) 

    result = subprocess.run(sys.argv[2:])
    return result.returncode


def run_envdo():
    config_path = utils.find_config()

    if not config_path.exists():
        config_path.write_text(EXAMPLE_CONFIG.strip())
    
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
        if len(sys.argv) <= 2:
            utils.print_error(f'Please specify a command to run (e.g., envdo {sys.argv[1]} echo "Hello, World!")')
            sys.exit(1) 

        config = utils.load_config(config_path)
        utils.select_env(config)

    elif sys.argv[1] in config.keys():
        if len(sys.argv) <= 2:
            utils.print_error(f'Please specify a command to run (e.g., envdo {sys.argv[1]} echo "Hello, World!")')
            sys.exit(1) 
        
        utils.set_env(sys.argv[1], config)

    elif sys.argv[1] in ('h', 'help', '-h', '--help'):
        utils.print_help()
        sys.exit(0)

    else:
        utils.print_help()
        sys.exit(1)


def main():
    try:
        run_envdo()
        return_code = run_command()
        sys.exit(return_code)
    except Exception as e:
        utils.print_error(f'Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
