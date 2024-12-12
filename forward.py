import json
import re
import sys

from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

from common import print, printerr, get_entity
from dataclasses import dataclass
from typing import Union

import api

def get_peer(chat_str: str):
    pattern = r'Peer(User|Channel)\((user|channel)_id=\d+\)'
    if re.match(pattern, chat_str):
        return eval(chat_str)
    raise ValueError(f'Invalid peer format: {chat_str}')

@dataclass
class Message:
    id: int
    peer: Union[PeerUser, PeerChat, PeerChannel]

    @staticmethod
    def parse(line: str) -> Union['Message', None]:
        data = line.split('\t', 3)
        if len(data) < 3:
            printerr('Invalid data length: `', repr(data), '`')
            return None
        try:
            msg_id, peer_type_s = int(data[0]), data[1]
            match peer_type_s:
                case 'user':
                    peer_type = PeerUser
                case 'chat':
                    peer_type = PeerChat
                case 'channel':
                    peer_type = PeerChannel
                case _:
                    printerr('Invalid peer type: ', peer_type)
                    return None
            peer_id = int(data[2])
        except ValueError as e:
            printerr('Error while parsing: ', repr(e))
            return None
        return Message(msg_id, peer_type(peer_id))

INVALID_ARGS_ERR = 1
TELEGRAM_ERR = 2

def main(args):
    if len(args) != 1:
        return INVALID_ARGS_ERR
    target = args[0]

    with TelegramClient('forward', api.id, api.hash) as client:
        try:
            target_entity = get_entity(client, target)
        except Exception as e:
            printerr('Failed to find entity for `', target, '`')
            return TELEGRAM_ERR

        # only parse valid lines
        try:
            for msg in filter(None, map(Message.parse, sys.stdin)):
                client.forward_messages(target_entity, msg.id, msg.peer)
        except KeyboardInterrupt:
            return

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
    printerr('  Program accepts lines with tab-separated fields:')
    printerr('  - id: int - message id')
    printerr('  - peer_type: str - user, channel, chat')
    printerr('  - peer_id: int - id of user, channel or chat')
    printerr('  - text: any - ignored')

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

