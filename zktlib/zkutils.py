from struct import pack, unpack
from datetime import datetime, date
from math import ceil

from zkconst import *

def reverseHex(hexstr):
    tmp = ''
    range_iter = ceil(len(hexstr)/2)

    for i in reversed( range(range_iter)):
        tmp += hexstr[i*2:(i*2)+2]

    return tmp

def encode_time(t):
    """Encode a timestamp send at the timeclock
    copied from zkemsdk.c - EncodeTime"""

    d = ( (t.year % 100) * 12 * 31 + ((t.month - 1) * 31) + t.day - 1) *\
         (24 * 60 * 60) + (t.hour * 60 + t.minute) * 60 + t.second

    return d


def decode_time(t):
    """Decode a timestamp retrieved from the timeclock
    copied from zkemsdk.c - DecodeTime"""

    second = int(t % 60)
    t = t / 60

    minute = int(t % 60)
    t = t / 60

    hour = int(t % 24)
    t = t / 24

    day = int(t % 31 + 1)
    t = t / 31

    month = int(t % 12 + 1)
    t = t / 12

    year = int(t + 2000)

    d = datetime(year, month, day, hour, minute, second)

    return d

def getPacketSize(obj_sent):
    """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
    indicating that data packets are to be sent

    Returns the amount of bytes that are going to be sent"""

    command = unpack('HHHH', obj_sent.data_recv[:8])[0]

    if command == CMD_PREPARE_DATA:
        size = unpack('I', obj_sent.data_recv[8:12])[0]
        return size
    else:
        return False
