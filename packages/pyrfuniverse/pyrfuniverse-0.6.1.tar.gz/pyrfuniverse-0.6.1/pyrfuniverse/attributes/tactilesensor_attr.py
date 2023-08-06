import pyrfuniverse.attributes as attr
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
import pyrfuniverse.utils.rfuniverse_utility as utility

def parse_message(msg: IncomingMessage) -> dict:
    this_object_data = {}
    this_object_data['force'] = msg.read_float32()
    return this_object_data
