import os
from envdo import utils


__all__ = ['find_envdo', 'load_envdo']


old_envs = os.environ.copy()


def find_envdo() -> str|None:
    '''Find the path to the envdo configuration file.

    Returns:
        str | None: The path to the configuration file if found, None otherwise.
    '''
    return utils.find_config()


def load_envdo(name: str, path: str|None = None) -> dict:
    '''Load and apply environment variables from a named configuration.

    Args:
        name: The name of the environment configuration to load.
        path: Optional path to the configuration file. If not provided,
              the default configuration file will be used.

    Returns:
        dict: The loaded environment variables as a dictionary.

    Raises:
        ValueError: If the specified name is not found in the configuration.
        FileNotFoundError: If the configuration file cannot be found or loaded.
    '''
    if path is None:
        path = find_envdo()

    config = utils.load_config(path)

    if name not in config:
        raise ValueError(f'{name} not found in environment configuration')

    env_dict = config[name]
    new_envs = old_envs
    old_envs.update(env_dict)
    os.environ = new_envs

    return dict(env_dict)
