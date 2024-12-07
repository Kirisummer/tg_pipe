import json
import re
import sys

from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

from common import print, printerr, get_entity
import api

def get_peer(chat_str: str):
    pattern = r'Peer(User|Channel)\((user|channel)_id=\d+\)'
    if re.match(pattern, chat_str):
        return eval(chat_str)
    raise ValueError(f'Invalid peer format: {chat_str}')

INVALID_ARGS_ERR = 1
TELEGRAM_ERR = 2

def main(args):
    if len(args) != 1:
        return INVALID_ARGS_ERR
    target = args[0]

    with TelegramClient('forwarder', api.id, api.hash) as client:
        try:
            target_entity = get_entity(client, target)
        except Exception as e:
            printerr('Failed to find entity for `', target, '`')
            return TELEGRAM_ERR

        for line in sys.stdin:
            line = line.strip()
            try:
                msg_dict = json.loads(line)
                peer = get_peer(msg_dict['chat'])
            except Exception as e:
                printerr('Invalid entry: `', line, '`: ', repr(e))
                continue
            client.forward_messages(target_entity, msg_dict['id'], peer)

def print_help(prog_name):
    printerr('Usage:')
    printerr('  ', prog_name, ' <target>')
    printerr('  ', prog_name, ' --help')
    printerr()
    printerr('Arguments:')
    printerr('  target: something that can be used to identify a dialog: user id, phone number, chat name')
    printerr('  --help: show this help')
    printerr()
    printerr('Input:')
    printerr('  Program accepts single-line JSON objects. Objects must contain:')
    printerr('  - id: int - message id')
    printerr('  - chat: str - Telethon peer representation, either PeerUser or PeerChannel with user_id or channel_id. Example: PeerUser(user_id=12345)')

if __name__ == '__main__':
    prog_name = sys.argv[0]
    args = sys.argv[1:]

    if '--help' in args:
        print_help(prog_name)
        sys.exit(INVALID_ARGS_ERR)
    else:
        ret = main(args)
        if ret == INVALID_ARGS_ERR:
            print_help(prog_name)
        sys.exit(ret)

