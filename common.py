from functools import cache
import sys

_print = print

def print(*args, **kwargs):
    _print(*args, **kwargs, sep='')

def printerr(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)

@cache
def get_entity(client: 'TelegramClient', name: str):
    entity = None
    try:
        entity = client.get_input_entity(name)
    except ValueError:
        printerr('Failed to get input entity for `', name, '`, searching for it in dialog list')
        # search for first dialog with matching name
        entity = next(filter(lambda dialog: dialog.name == name, client.iter_dialogs()))
    printerr('Found entity for `', name, '`: ', entity)
    return entity

