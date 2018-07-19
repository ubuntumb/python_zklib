from socket import *

import sys
import select
import errno
import time

from struct import pack, unpack
from datetime import datetime, date

from zkconnect import *
from zkversion import *
from zkos import *
from zkextendfmt import *
from zkextendoplog import *
from zkplatform import *
from zkworkcode import *
from zkssr import *
from zkpin import *
from zkface import *
from zkserialnumber import *
from zkdevice import *
from zkuser import *
from zkattendance import *
from zktime import *
from zkprepare import *
from zkrefreshdata import *
from zkfreedata import *
from zkrestart import *
from zkAtt import *

class ZKLib:

    def __init__(self, ip, port):
        self.address = (ip, port)
        self.zkclient = socket(AF_INET, SOCK_DGRAM)
        self.zkclient.settimeout(10)
        self.session_id = 0
        self.reply_id = 0
        self.userdata = []
        self.attendancedata = []


    def createChkSum(self, p):
        """This function calculates the chksum of the packet to be sent to the
        time clock

        Copied from zkemsdk.c"""
        l = len(p)
        chksum = 0
        while l > 1:
            chksum += unpack('H', pack('BB', p[0], p[1]))[0]

            p = p[2:]
            if chksum > USHRT_MAX:
                chksum -= USHRT_MAX
            l -= 2


        if l:
            chksum = chksum + p[-1]

        while chksum > USHRT_MAX:
            chksum -= USHRT_MAX

        chksum = ~chksum

        while chksum < 0:
            chksum += USHRT_MAX

        return pack('H', chksum)


    def createHeader(self, command, chksum, session_id, reply_id,
                                command_string):
        """This function puts a the parts that make up a packet together and
        packs them into a byte string"""

        if(isinstance(command_string, str)):
            command_string = command_string.encode()

        buf = pack('HHHH', command, chksum,
            session_id, reply_id) + command_string

        buf = unpack('8B'+'%sB' % len(command_string), buf)

        chksum = unpack('H', self.createChkSum(buf))[0]
        #print unpack('H', self.createChkSum(buf))
        reply_id += 1
        if reply_id >= USHRT_MAX:
            reply_id -= USHRT_MAX

        buf = pack('HHHH', command, chksum, session_id, reply_id)
        return buf + command_string


    def checkValid(self, reply):
        """Checks a returned packet to see if it returned CMD_ACK_OK,
        indicating success"""
        command = unpack('HHHH', reply[:8])[0]

        print('COMMNAD', command)

        if command == CMD_ACK_UNAUTH:
            return zkconnect_with_pass(self,0)
        elif command == CMD_ACK_OK:
            return True
        else:
            return False

    def decode_result_bytes_to_string(func):
        def verify_value_result(*args, **kwargs):
            result = func(*args, **kwargs)

            try:
                if(isinstance(result, bytes)):
                    return result.decode()
            except Exception as e:
                print('Error to decode value ', e)

            return result
        return verify_value_result

    def connect(self):
        return zkconnect(self)

    def disconnect(self):
        return zkdisconnect(self)

    @decode_result_bytes_to_string
    def version(self):
        return zkversion(self)

    @decode_result_bytes_to_string
    def osversion(self):
        return zkos(self)

    def extendFormat(self):
        return zkextendfmt(self)

    def extendOPLog(self, index=0):
        return zkextendoplog(self, index)

    @decode_result_bytes_to_string
    def platform(self):
        return zkplatform(self)

    @decode_result_bytes_to_string
    def fmVersion(self):
        return zkplatformVersion(self)

    @decode_result_bytes_to_string
    def workCode(self):
        return zkworkcode(self)

    @decode_result_bytes_to_string
    def ssr(self):
        return zkssr(self)

    @decode_result_bytes_to_string
    def pinWidth(self):
        return zkpinwidth(self)

    @decode_result_bytes_to_string
    def faceFunctionOn(self):
        return zkfaceon(self)

    @decode_result_bytes_to_string
    def serialNumber(self):
        return zkserialnumber(self)

    @decode_result_bytes_to_string
    def deviceName(self):
        return zkdevicename(self)

    @decode_result_bytes_to_string
    def enableDevice(self):
        return zkenabledevice(self)

    def disableDevice(self):
        return zkdisabledevice(self)

    def restartDevice(self):
        return zkrestart(self)

    def poweroffDevice(self):
        return zkpoweroff(self)

    def getUser(self):
        return zkgetuser(self)

    def setUser(self, uid, userid, name, password, role):
        return zksetuser(self, uid, userid, name, password, role)

    def clearUser(self):
        return zkclearuser(self)

    def clearAdmin(self):
        return zkclearadmin(self)

    def enrollUser(self, uid):
        return zkenrolluser(self, uid)

    def getAttendance(self):
        return zkgetattendance(self)

    def clearAttendance(self):
        return zkclearattendance(self)

    @decode_result_bytes_to_string
    def setTime(self, t):
        return zksettime(self, t)

    def getTime(self):
        return zkgettime(self)

    def prepareData(self):
        return zkprepare(self)

    def refreshData(self):
        return zkrefreshdata(self)

    def freeData(self):
        return zkfreedata(self)

    def reboot(self):
        return zkrestart(self)

    def testatt(self):
        return zkAtt(self)
