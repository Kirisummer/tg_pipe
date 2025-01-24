from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum
from dataclasses import dataclass
import sys

from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChannel, PeerChat

from common import add_api_arg, add_session_arg, get_entity, print, printerr

parser = ArgumentParser(description='Listen to Telegram sources (channels, users, chats) and print them',
                        epilog='Program prints tab-separated lists to identify the peer and message to forward\n' \
                                '  - msg_id: int - id of message to forward\n' \
                                '  - peer_type: (user|chat|channel) - type of a peer\n' \
                                '  - peer_id: int - id of a peer\n' \
                                '  - message text: str - text of the message',
                        formatter_class=RawTextHelpFormatter)
parser.add_argument('sources', nargs='+', help='Sources to listen. Can be usernames, phone numbers, chat names, etc.')
add_api_arg(parser)
add_session_arg(parser)
args = parser.parse_args()

with TelegramClient(args.session, args.api.id, args.api.hash) as client:
    try:
        entities = [get_entity(client, source) for source in args.sources]
    except Exception as e:
        printerr(e.args[0])
        sys.exit(1)

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
