from dataclasses import dataclass
from functools import cache
from itertools import starmap
from typing import Pattern, Iterable
import json
import re
import sys

from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChannel, PeerChat

from common import print, printerr, get_entity
import api

INVALID_ARGS_ERR = 1
TELEGRAM_ERR = 2

def main(args: list[str]):
    if not args:
        printerr('No sources given')
        return INVALID_ARGS_ERR

    with TelegramClient('listen', api.id, api.hash) as client:
        try:
            entities = [get_entity(client, source) for source in args]
        except Exception as e:
            printerr(e.args[0])
            return TELEGRAM_ERR

        @client.on(events.NewMessage(chats=entities))
        async def handler(event):
            message = event.message
            peer_id = message.peer_id
            match peer_id:
                case PeerUser():
                    chat_type = 'user'
                    chat_id = peer_id.user_id
                case PeerChannel():
                    chat_type = 'channel'
                    chat_id = peer_id.channel_id
                case PeerChat():
                    chat_type = 'chat'
                    chat_id = peer_id.chat_id
                case _:
                    chat_type = 'unknown'
                    chat_id = str(peer_id)
            print(message.id, chat_type, chat_id, message.text, sep='\t')

        client.run_until_disconnected()

def print_help(prog_name):
    printerr('Usage:')
    printerr('  ', prog_name, ' <source> [<source> [...]]')
    printerr('  ', prog_name, ' --help')
    printerr()
    printerr('Arguments:')
    printerr('  source: something that can be used to identify a dialog: user id, phone number, chat name')
    printerr('  --help: show this help')

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

