from functools import cache
from typing import Union, Tuple

from telethon.tl.types import PeerUser, PeerChannel, PeerChat

from print import printerr

@cache
def get_entity(client: 'TelegramClient', name: str):
    entity = None
    try:
        entity = client.get_input_entity(name)
    except Exception:
        printerr('Failed to get input entity for `', name, '`, searching for it in dialog list')
        # search for first dialog with matching name
        try:
            entity = next(filter(lambda dialog: dialog.name == name, client.iter_dialogs()))
        except StopIteration:
            raise ValueError(f'Failed to find entity for `{name}`')
    printerr('Found entity for `', name, '`: ', entity)
    return entity

def unpack_peer(peer_id: Union[PeerUser,PeerChannel,PeerChat]) -> Tuple[str, int] | None:
    match peer_id:
        case PeerUser():
            return 'user', peer_id.user_id
        case PeerChannel():
            return 'channel', peer_id.channel_id
        case PeerChat():
            return 'chat', peer_id.channel_id
        case _:
            return None

def pack_peer(peer_type_s: str, peer_id: int):
    match peer_type_s:
        case 'user':
            return PeerUser(peer_id)
        case 'channel':
            return PeerChannel(peer_id)
        case 'chat':
            return PeerChat(peer_id)
        case _:
            return None
