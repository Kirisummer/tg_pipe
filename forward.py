from argparse import ArgumentParser, RawTextHelpFormatter
from dataclasses import dataclass
from typing import Union
import re
import sys

from telethon.sync import TelegramClient

from parsers import add_api_arg, add_session_arg
from tg_utils import pack_peer, get_entity
from print import printerr

@dataclass
class Message:
    id: int
    peer: Union['PeerUser', 'PeerChat', 'PeerChannel']

    @staticmethod
    def parse(line: str) -> Union['Message', None]:
        data = line.split('\t', 3)
        if len(data) < 3:
            printerr('Invalid data length: `', repr(data), '`')
            return None
        try:
            msg_id, peer_type_s, peer_id = int(data[0]), data[1], int(data[2])
        except ValueError as e:
            printerr('Error while parsing: ', repr(e))
            return None
        peer = pack_peer(peer_type_s, peer_id)
        if not peer:
            return None
        return Message(msg_id, peer)

parser = ArgumentParser(description='Forward messages to a Telegram channel, chat or user',
                        epilog='Program reads tab-separated lists to identify the peer and message to forward\n' \
                                '  - msg_id: int - id of message to forward\n' \
                                '  - peer_type: (user|chat|channel) - type of a peer\n' \
                                '  - peer_id: int - id of a peer\n' \
                                'Further fields are ignored.',
                        formatter_class=RawTextHelpFormatter)
parser.add_argument('target',
                    help='Telegram channel, char or user to forward messages to.' \
                         'Can be usernames, phone numbers, chat names, etc.')

add_api_arg(parser)
add_session_arg(parser)
args = parser.parse_args()

with TelegramClient(args.session, args.api.id, args.api.hash) as client:
    try:
        target_entity = get_entity(client, args.target)
    except Exception as e:
        printerr('Failed to find entity for `', target, '`')
        sys.exit(1)

    # only parse valid lines
    try:
        for msg in filter(None, map(Message.parse, sys.stdin)):
            client.forward_messages(target_entity, msg.id, msg.peer)
    except KeyboardInterrupt:
        pass
