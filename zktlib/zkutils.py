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
    t = t // 60

    minute = int(t % 60)
    t = t // 60

    hour = int(t % 24)
    t = t // 24

    day = int(t % 31 + 1)
    t = t // 31

    month = int(t % 12 + 1)
    t = t // 12

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

def make_commkey(key, session_id, ticks=50):
    """take a password and session_id and scramble them to send to the time
    clock.
    copied from commpro.c - MakeKey"""
    key = int(key)
    session_id = int(session_id)
    k = 0
    for i in range(32):
        if (key & (1 << i)):
            k = (k << 1 | 1)
        else:
            k = k << 1
    k += session_id

    k = pack(b'I', k)
    k = unpack(b'BBBB', k)
    k = pack(
        b'BBBB',
        k[0] ^ ord('Z'),
        k[1] ^ ord('K'),
        k[2] ^ ord('S'),
        k[3] ^ ord('O'))
    k = unpack(b'HH', k)
    k = pack(b'HH', k[1], k[0])

    B = 0xff & ticks
    k = unpack(b'BBBB', k)
    k = pack(
        b'BBBB',
        k[0] ^ B,
        k[1] ^ B,
        B,
        k[3] ^ B)
    return k
