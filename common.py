from functools import cache
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys

# Types with validation for ArgumentParser arguments ###########################

def regular_file(arg: str) -> Path:
    path = Path(arg)
    if not path.is_file():
        raise ValueError('File does not exist or is not a regular file')
    return path

def api_file(arg: str) -> 'TgAPI':
    # Verify that API file is a regular file that exists
    path = regular_file(arg)

    # Load API file as module
    spec = spec_from_file_location('api', path)
    api = module_from_spec(spec)
    spec.loader.exec_module(api)

    # Verify that module has id and hash
    if hasattr(api, 'id') and hasattr(api, 'hash'):
        return api
    raise ValueError('API file does not have id or hash')

def absent_file(arg: str) -> Path:
    path = Path(arg)
    if not path.exists():
        return path
    raise ValueError('File exists')

# Functions that add arguments to ArgumentParser ###############################

def add_api_arg(parser: 'ArgumentParser'):
    parser.add_argument('-a', '--api', type=api_file, help='Path to the file with Telegram API id and hash', required=True)

def add_session_arg(parser: 'ArgumentParser'):
    parser.add_argument('-s', '--session', type=regular_file, help='Path to the session file', required=True)

# Prints with custom defaults ##################################################

_print = print

def print(*args, sep='', **kwargs):
    _print(*args, sep=sep, **kwargs)

def printerr(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

# Telegram entity getter #######################################################

@cache
def get_entity(client: 'TelegramClient', name: str):
    entity = None
    try:
        entity = client.get_input_entity(name)
    except Exception:
        printerr('Failed to get input entity for `', name, '`, searching for it in dialog list')
        # search for first dialog with matching name
        try:
            entity = next(filter(lambda dialog: dialog.name == name, client.iter_dialogs()))
        except StopIteration:
            raise ValueError(f'Failed to find entity for `{name}`')
    printerr('Found entity for `', name, '`: ', entity)
    return entity

