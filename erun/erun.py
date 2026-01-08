import sys
import subprocess

from erun import utils


config_path = '~/.erun/config.json'


def run_command(argv: list):
    subprocess.run(argv[2:], check=False, shell=True)


def run_erun(config_path):
    if len(sys.argv) <= 1:
        utils.print_help()
        sys.exit(0)
    
    config = utils.load_config(config_path)

    if sys.argv[1] in ('l', 'list'):
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
    try:
        run_erun(config_path)
    except Exception as e:
        utils.print_error(f'Error: {e}')
        sys.exit(1)

    run_command(sys.argv)
    sys.exit(0)


if __name__ == '__main__':
    run()
