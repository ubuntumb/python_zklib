import sys
sys.path.append("zktlib")

from zktlib import zklib as zkt
import time
from datetime import datetime
import zkconst


zk = zkt.ZKLib("192.168.1.201", 4370)

ret = zk.connect()

print ("connection:", ret)

if ret == True:
    #print "Disable Device", zk.disableDevice()

    print ("ZK Version:", zk.version())
    print ("OS Version:", zk.osversion())
    """
    print "Extend Format:", zk.extendFormat()
    print "Extend OP Log:", zk.extendOPLog()
    """

    print ("Platform:", zk.platform())
    print ("Platform Version:", zk.fmVersion())
    print ("Work Code:", zk.workCode())
    print ("Work Code:", zk.workCode())
    print ("SSR:", zk.ssr())
    print ("Pin Width:", zk.pinWidth())
    print ("Face Function On:", zk.faceFunctionOn())
    print ("Serial Number:", zk.serialNumber())
    print ("Device Name:", zk.deviceName())

    data_user = zk.getUser()
    print ("User size:", len(data_user))
    #print ("Get User:", data_user)
    if data_user:
        for uid in data_user:

            if data_user[uid][2] == 14:
                level = 'Admin'
            else:
                level = 'User'
            print ( "[UID %d]: ID: %s, Name: %s, Level: %s, Password: %s" % ( uid, data_user[uid][0], data_user[uid][1], level, data_user[uid][3]  ) )
            #print(uid, data_user[uid])

        #zk.setUser(uid=61, userid='41', name='Dony Wahyu Isp', password='123456', role=zkconst.LEVEL_ADMIN)

    attendance = zk.getAttendance()

    if ( attendance ):
        print('Attendance size', len(attendance))
        for lattendance in attendance:
            if lattendance[1] == 15:
                state = 'Check In'
            elif lattendance[1] == 0:
                state = 'Check Out'
            else:
                state = 'Undefined'

            print('att', lattendance)
            #print ("date %s, Jam %s: %s, Status: %s" % ( lattendance[2].date(), lattendance[2].time(), lattendance[0], state ))

    # print "Clear Attendance:", zk.clearAttendance()

    #zk.setUser(67, '67', 'Shubhamoy Chakrabarty', '', 0)
    #zk.enrollUser('67')
    print ("Enable Device", zk.enableDevice())
    print ("Set Time:", zk.setTime(datetime.now()))
    print ("Get Time:", zk.getTime())

    #print("Restart Device", zk.restartDevice())
    print ("Disconnect:", zk.disconnect())
