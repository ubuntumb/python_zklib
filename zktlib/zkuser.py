from struct import pack, unpack, Struct
import binascii
import codecs
from datetime import datetime, date

from zkconst import *
from zkutils import getPacketSize


def zksetuser(self, uid, userid, name, password, role):
    """Start a connection with the time clock"""
    command = CMD_SET_USER
    command_string = pack('sxs8s28ss7sx8s16s', chr( uid ).encode(), chr(role).encode(), password.encode(), name.encode(), chr(1).encode(), b'', userid.encode(), b'' )
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
        print ('Error to set User, ', e)
        return False


def zkgetuser(self):
    """Start a connection with the time clock"""
    command = CMD_USERTEMP_RRQ
    command_string = '\x05'
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)
    #print ("buffer encode", buf)
    #self.data_recv, addr = self.zkclient.recvfrom(1024)
    #print ("data_recv : ", self.data_recv[8:], "\n from ", addr)
    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)

        if getPacketSize(self):
            bytes = getPacketSize(self)

            while bytes > 0:
                data_recv, addr = self.zkclient.recvfrom(1032)
                self.userdata.append(data_recv)
                bytes -= 1024

            self.session_id = unpack('HHHH', self.data_recv[:8])[2]
            data_recv = self.zkclient.recvfrom(8)

        users = {}
        if len(self.userdata) > 0:
            # The first 4 bytes don't seem to be related to the user
            for x in range(len(self.userdata)):
                if x > 0:
                    self.userdata[x] = self.userdata[x][8:]

            userdata = bytearray(self.userdata[0])
            
            for usr in self.userdata[1:]:
                userdata = userdata + usr

            userdata = userdata[11:]

            while len(userdata) > 72:

                uid, role, password, name, userid = unpack( '2s2s8s28sx31s', userdata.ljust(72)[:72] )
                uid = int(uid.hex(),16)
                name = name.split(b'\x00', 1)[0].decode(errors="ignore") # Clean up some messy characters from the user name
                password = password.strip(b'\x00|\x01\x10x').decode(errors='ignore')
                userid = userid.strip(b'\x00|\x01\x10x').decode(errors='ignore')
                role = int(role.hex(), 16)

                #print(uid, name, role , password, userid)

                if name.strip() == "":
                    name = uid

                users[uid] = (userid, name, role, password)
                userdata = userdata[72:]

        return users
    except Exception as e:
        print('Error to get User data, ', e)
        return False


def zkclearuser(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_DATA
    command_string = ''
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
    except:
        return False


def zkclearadmin(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_ADMIN
    command_string = ''
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
    except:
        return False

def zkenrolluser(self, uid):
    '''Start Remote Fingerprint Enrollment'''

    command = CMD_STARTENROLL
    command_string = pack('2s', uid.encode())
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)

    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)
        self.session_id = unpack('HHHH', self.data_recv[:8])[2]
        return self.data_recv[8:]
    except Exception as e :
        print ("Error Enroll User, ", e)
        return False
