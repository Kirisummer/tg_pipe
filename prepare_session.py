from argparse import ArgumentParser
from pathlib import Path

from telethon.sync import TelegramClient

from parsers import add_api_arg

parser = ArgumentParser(description='Create a session file or try to re-login')
parser.add_argument('session', type=Path, help='Path to a session file')
add_api_arg(parser)
args = parser.parse_args()

with TelegramClient(args.session, args.api.id, args.api.hash):
    pass
