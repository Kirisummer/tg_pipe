from collections.abc import Callable
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# File types ###########################################3#######################

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

# Message formats ##############################################################

def base64_fmt(s: str) -> str:
    return b64encode(s.encode('utf8')).decode('ascii')

def message_format(name: str) -> Callable[[str], str]:
    match name:
        case 'repr':
            return repr
        case 'base64':
            return base64_fmt
        case _:
            raise ValueError(f'Invalid message format: {name}')

# Functions that add arguments to ArgumentParser ###############################

def add_api_arg(parser: 'ArgumentParser'):
    parser.add_argument('-a', '--api', type=api_file, help='Path to the file with Telegram API id and hash', required=True)

def add_session_arg(parser: 'ArgumentParser'):
    parser.add_argument('-s', '--session', type=regular_file, help='Path to the session file', required=True)

def add_msg_format_arg(parser: 'ArgumentParser'):
    parser.add_argument('-f', '--msg-fmt', type=message_format,
                        choices=(repr, base64_fmt), default='repr',
                        help='Format options for message text')
