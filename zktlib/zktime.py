from struct import pack, unpack
from datetime import datetime, date

from zkconst import *
from zkutils import reverseHex, encode_time, decode_time


def zksettime(self, t):
    """Start a connection with the time clock"""
    command = CMD_SET_TIME
    command_string = pack('I',encode_time(t))
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print buf.encode("hex")
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except Exception as e:
        print('Error to set time,', e)
        return False


def zkgettime(self):
    """Start a connection with the time clock"""
    command = CMD_GET_TIME
    command_string = ''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)

    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return decode_time( int( reverseHex( self.data_recv[8:].hex() ), 16 ) )
    except Exception as e:
        print('Error to get time,', e)
        return False
