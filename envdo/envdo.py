import sys
import subprocess
from pathlib import Path

from envdo import utils


VERSION = '0.0.1'


def run_command(argv: list):
    subprocess.run(argv[2:], check=False, shell=True)


def run_envdo(config_path):
    if len(sys.argv) <= 1:
        utils.print_help()
        sys.exit(0)

    try: 
        config = utils.load_config(config_path)
    except Exception as e:
        utils.print_error(f'Error loading config. Please check the file format. Path: {config_path}')
        sys.exit(1)

    if sys.argv[1] in ('-v', '--version'):
        print(VERSION)
        sys.exit(0)

    elif sys.argv[1] in ('l', 'list'):
        utils.list_env(config)
        sys.exit(0)

    elif sys.argv[1] in ('s', 'select'):
        config = utils.load_config(config_path)
        utils.select_env(config)

    elif sys.argv[1] in config.keys():
        utils.set_env(sys.argv[1], config)

    else:
        utils.print_help()
        sys.exit(0)


def run():
    config_path = Path('./.envdo.json')

    if not config_path.exists():
        config_path = Path('~/.envdo.json').expanduser()

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.touch()
    
    try:
        run_envdo(config_path)
    except Exception as e:
        utils.print_error(f'Error: {e}')
        sys.exit(1)

    run_command(sys.argv)
    sys.exit(0)


if __name__ == '__main__':
    run()
