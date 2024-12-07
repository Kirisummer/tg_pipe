from dataclasses import dataclass
from functools import cache
from itertools import starmap
from typing import Pattern, Iterable
import json
import re
import sys

from telethon.sync import TelegramClient, events

from common import print, printerr, get_entity
import api

@dataclass(frozen=True)
class Target:
    name: str
    patterns: tuple[Pattern]

    @staticmethod
    def __regex(pattern: str) -> Pattern:
        try:
            return re.compile(pattern, re.I)
        except re.error as e:
            raise ValueError(f'Failed to compile regex `{pattern}`: {repr(e)})')

    @staticmethod
    def make(name: str, patterns: Iterable[str]):
        re_patterns = tuple(map(Target.__regex, patterns))
        return Target(name, re_patterns)

    def validate(self, text: str) -> bool:
        return any(map(lambda pattern: re.match(pattern, text), self.patterns))

INVALID_ARGS_ERR = 1
TELEGRAM_ERR = 2

def main(args: list[str]):
    # 1 pattern per chat
    # make sure at least one source is present, and each source has a filter
    if len(args) < 2 or len(args) % 2 == 1:
        printerr('Invalid number of arguments')
        return INVALID_ARGS_ERR

    def make_nested(src_list: Iterable[str]) -> Iterable[tuple[str]]:
        for item in src_list:
            yield (item,)
    try:
        targets = tuple(starmap(Target.make, zip(args[0::2], make_nested(args[1::2]))))
    except Exception as e:
        printerr('Failed to create source/filter pairs: ', repr(e))
        return INVALID_ARGS_ERR

    with TelegramClient('filter', api.id, api.hash) as client:
        for target in targets:
            try:
                entity = get_entity(client, target.name)
            except Exception as e:
                printerr('Failed to find entity for `', target.name, '`')
                return TELEGRAM_ERR

            @client.on(events.NewMessage(chats=entity, pattern=target.validate))
            async def handler(event):
                msg_dict = {
                        'id': event.message.id,
                        'chat': str(event.message.peer_id),
                        'text': event.message.text
                }
                print(json.dumps(msg_dict, ensure_ascii=False))

        client.run_until_disconnected()

def print_help(prog_name):
    printerr('Usage:')
    printerr('  ', prog_name, ' <source> <filter> [<source> <filter> [...]]')
    printerr('  ', prog_name, ' --help')
    printerr()
    printerr('Arguments:')
    printerr('  source: something that can be used to identify a dialog: user id, phone number, chat name')
    printerr('  filter: regex to match text with')
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

