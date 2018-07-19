from struct import pack, unpack
from datetime import datetime, date

from zkconst import *
from zkutils import make_commkey

def zkconnect(self):
    """Start a connection with the time clock"""
    command = CMD_CONNECT
    command_string = ''
    chksum = 0
    session_id = 0
    reply_id = -1 + USHRT_MAX

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)

    self.zkclient.sendto(buf, self.address)

    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        self.reply_id = unpack('HHHH', self.data_recv[:8])[3]

        return self.checkValid( self.data_recv )
    except Exception as e:
        print('Error to connect ', e)
        return False


def zkconnect_with_pass(self, password=0):
    """Start a connection to the time clock with password"""
    command = CMD_AUTH
    command_string = make_commkey(password, self.session_id)
    chksum = 0

    buf = self.createHeader(command, chksum, self.session_id,
        self.reply_id, command_string)

    print('sendto', repr(buf))
    self.zkclient.sendto(buf, self.address)
    print('sendEnd', 'Ok')
    try:
        print('data_recv sendto', repr(buf))
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        print('sendto', repr(buf))
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        self.reply_id = unpack('HHHH', self.data_recv[:8])[3]

        return self.checkValid( self.data_recv )
    except Exception as e:
        print('Error to connect with password %s' % (password), e)
        return False

def zkdisconnect(self):
    """Disconnect from the clock"""
    command = CMD_EXIT
    command_string = ''
    chksum = 0
    session_id = self.session_id

    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    try:
        self.zkclient.sendto(buf, self.address)
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        return self.checkValid( self.data_recv )
    except Exception as e:
        print('Error to disconnect, ', e)
        return False
