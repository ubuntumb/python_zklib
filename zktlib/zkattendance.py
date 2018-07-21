from struct import pack, unpack
from datetime import datetime, date

from zkconst import *
from zkutils import reverseHex, decode_time, getPacketSize

import pprint
pp = pprint.PrettyPrinter(indent=4)

def zkgetattendance(self):
    """Start a connection with the time clock"""
    command = CMD_ATTLOG_RRQ
    command_string = ''
    chksum = 0
    session_id = self.session_id
    reply_id = unpack('HHHH', self.data_recv[:8])[3]

    buf = self.createHeader(command, chksum, session_id,
        reply_id, command_string)
    self.zkclient.sendto(buf, self.address)

    try:
        self.data_recv, addr = self.zkclient.recvfrom(1024)

        if getPacketSize(self):
            bytes = getPacketSize(self)
            while bytes > 0:
                data_recv, addr = self.zkclient.recvfrom(1032)
                self.attendancedata.append(data_recv)
                bytes -= 1024

            self.session_id = unpack('HHHH', self.data_recv[:8])[2]
            data_recv = self.zkclient.recvfrom(8)

        attendance = []
        if len(self.attendancedata) > 0:
            # The first 4 bytes don't seem to be related to the user
            for x in range(len(self.attendancedata)):
                if x > 0:
                    self.attendancedata[x] = self.attendancedata[x][8:]

            attendancedata = bytearray(self.attendancedata[0])
            
            for att in self.attendancedata[1:] :
                attendancedata = attendancedata + att

            attendancedata = attendancedata[14:]

            while len(attendancedata):

                uid, state, timestamp, space =  unpack( '24s1s4s11s', attendancedata.ljust(40)[:40] )
                uid = uid.split(b'\x00', 1)[0].decode(errors="ignore")  # Clean up some messy characters from the user name

                attendance.append((uid, int( state.hex(), 16 ), decode_time( int( reverseHex(timestamp.hex()), 16 ) ) ) )

                attendancedata = attendancedata[40:]

            return attendance
    except Exception as e:
        print("Error to get Attendance data ", e)
        return False


def zkclearattendance(self):
    """Start a connection with the time clock"""
    command = CMD_CLEAR_ATTLOG
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
