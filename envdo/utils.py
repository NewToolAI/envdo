import os
import json
from pathlib import Path

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt


def find_config():
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        config_path = parent / '.envdo.json'
        if config_path.exists():
            return config_path
    
    config_path = Path('~/.envdo.json').expanduser()
    
    if config_path.exists():
        return config_path
    else:
        return None


def load_config(path: str):
    path = Path(path).expanduser()

    if path.exists():
        config = json.loads(path.read_text())
        return config

    raise FileNotFoundError(f'{path} not found')


def list_env(config: dict):
    if not config:
        Console().print('[yellow]No configuration found[/yellow]')
        return
    
    console = Console()
    table = Table(
        title=None,
        show_header=True,
        header_style='bold cyan',
        border_style='bright_blue',
        box=box.ROUNDED
    )
    
    table.add_column('#', style='bold white', no_wrap=True, width=3, justify='right')
    table.add_column('Config Name', style='bold magenta', no_wrap=True, width=15)
    table.add_column('Environment Variable', style='green', width=25)
    table.add_column('Value', style='yellow', width=40)
    
    sensitive_keywords = ['TOKEN', 'KEY', 'PASSWORD', 'SECRET', 'AUTH', 'CREDENTIAL']
    
    config_names = list(config.keys())
    for idx, (config_name, env_vars) in enumerate(config.items(), start=1):
        first_row = True
        
        for key, value in env_vars.items():
            is_sensitive = any(keyword in key.upper() for keyword in sensitive_keywords)
            display_value = '***' if is_sensitive else value
            
            index_display = str(idx) if first_row else ''
            name_display = f'[bold]{config_name}[/bold]' if first_row else ''
            table.add_row(index_display, name_display, key, display_value)
            first_row = False
        
        if idx < len(config_names):
            table.add_row('', '', '', '')  # Empty row for spacing

    panel = Panel(
        table,
        title='[bold magenta]🔧 Environment Configurations[/bold magenta]',
        border_style='bright_green',
        padding=(1, 2)
    )
    
    console.print(panel)


def set_env(name: str, config: dict):
    console = Console()
    
    if name not in config:
        console.print(f'[bold red]✗[/bold red] Configuration "{name}" not found. Available: {", ".join(config.keys())}')
        return None
    
    selected_config = config[name]
    os.environ.update(selected_config)
    
    table = Table(
        title=None,
        show_header=True,
        header_style='bold cyan',
        border_style='green',
        box=box.ROUNDED
    )
    
    table.add_column('Environment Variable', style='cyan', width=25)
    table.add_column('Value', style='yellow', width=40)
    table.add_column('Status', style='green', width=10, justify='center')
    
    sensitive_keywords = ['TOKEN', 'KEY', 'PASSWORD', 'SECRET', 'AUTH', 'CREDENTIAL', 'API']
    
    for key, value in selected_config.items():
        is_sensitive = any(keyword in key.upper() for keyword in sensitive_keywords)
        display_value = '***' if is_sensitive else value
        table.add_row(key, display_value, '✓')
    
    panel = Panel(
        table,
        title=f'[bold magenta]🚀 Environment Selected: {name}[/bold magenta]',
        border_style='bright_green',
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print(f'[bold green]✓ Successfully applied {len(selected_config)} environment variables[/bold green]\n')
    
    return selected_config


def select_env(config: dict):
    console = Console()
    
    if not config:
        console.print('[yellow]No configuration found[/yellow]')
        return False
    
    list_env(config)
    
    config_names = list(config.keys())
    
    console.print()
    choice = Prompt.ask(
        '[bold cyan]Select configuration by number[/bold cyan]',
        choices=[str(i) for i in range(1, len(config_names) + 1)],
        show_choices=False
    )
    
    selected_index = int(choice) - 1
    selected_name = config_names[selected_index]
    
    return set_env(selected_name, config)


def print_error(message: str):
    console = Console()
    console.print(f'[bold red]✗[/bold red] {message}')


def print_help():
    console = Console()
    
    help_table = Table(
        title=None,
        show_header=False,
        border_style='cyan',
        box=box.ROUNDED,
        padding=(0, 2)
    )
    
    help_table.add_column('Command', style='bold cyan', width=37)
    help_table.add_column('Description', style='white', width=55)
    
    help_table.add_row('[bold]envdo name command[/bold]', 'Activate environment by name (e.g., envdo dev claude)')
    help_table.add_row('[bold]envdo s|select|i|interactive command[/bold]', 'Select and activate an environment interactively')
    help_table.add_row('[bold]envdo l|ls|list[/bold]', 'List all configured environments')
    help_table.add_row('[bold]envdo h|help|-h|--help[/bold]', 'Show this help message')
    
    panel = Panel(
        help_table,
        title='[bold magenta]⚙️  envdo - Help[/bold magenta]',
        border_style='bright_blue',
        padding=(1, 2)
    )
    
    console.print(panel)


if __name__ == '__main__':
    config = load_config('~/.envdo.json')
    select_env(config)
