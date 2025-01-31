from argparse import ArgumentParser, RawTextHelpFormatter
from base64 import b64encode
from itertools import islice
import sys

from telethon.sync import TelegramClient

from parsers import add_api_arg, add_session_arg, add_msg_format_arg
from tg_utils import get_entity, unpack_peer
from print import print, printerr

parser = ArgumentParser(description='Get certain number of messages from Telegram source (channel, user, chat) and print them',
                        epilog='Program prints tab-separated lists to identify the peer and message to forward\n' \
                                '  - msg_id: int - id of message to forward\n' \
                                '  - peer_type: (user|chat|channel) - type of a peer\n' \
                                '  - peer_id: int - id of a peer\n' \
                                '  - message text: str - text of the message',
                        formatter_class=RawTextHelpFormatter)
parser.add_argument('source', help='Source to print. Can be a username, phone number, chat name, etc.')
parser.add_argument('-n', '--count', type=int, default=10, help='Amount of messages to print. Default is 10.')
add_msg_format_arg(parser)
add_api_arg(parser)
add_session_arg(parser)
args = parser.parse_args()

with TelegramClient(args.session, args.api.id, args.api.hash) as client:
    try:
        entity = get_entity(client, args.source)
    except Exception as e:
        printerr(e.args[0])
        sys.exit(1)

    for message in reversed(list(client.iter_messages(entity, limit=args.count))):
        peer_type, peer_id = unpack_peer(message.peer_id)
        print(message.id, peer_type, peer_id, args.msg_fmt(message.text), sep='\t')
