import pyrfuniverse.attributes as attr
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
import pyrfuniverse.utils.rfuniverse_utility as utility


def parse_message(msg: IncomingMessage) -> dict:
    this_object_data = {}
    return this_object_data


def SetPositions(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'positions']
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('SetPositions')
    point_count = len(kwargs['positions'])
    msg.write_int32(point_count)
    for i in range(point_count):
        msg.write_float32(kwargs['positions'][i][0])
        msg.write_float32(kwargs['positions'][i][1])
        msg.write_float32(kwargs['positions'][i][2])

    return msg

def SetColor(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'color']
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()
    msg.write_int32(kwargs['id'])
    msg.write_string('SetColor')
    for i in range(4):
        msg.write_float32(kwargs['color'][i])

    return msg

def SetWidth(kwargs: dict) -> OutgoingMessage:
    compulsory_params = ['id', 'width']
    utility.CheckKwargs(kwargs, compulsory_params)

    msg = OutgoingMessage()

    msg.write_int32(kwargs['id'])
    msg.write_string('SetWidth')
    msg.write_float32(kwargs['width'])

    return msg


