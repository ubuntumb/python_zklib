# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("zktlib")

from zktlib import zklib as zkt
import time
from datetime import datetime
import zkconst

from zkutils import DefaultConnection
from zkmodel import AttModel, AttReloj


def collect_att_log(path_config_file=None):
    """Collect attendance log"""

    if not path_config_file:
        real_path = os.path.dirname(os.path.realpath(__file__))
        path_config_file = os.path.join(real_path, "config.ini")

    print ("path_config_file", path_config_file)
    conn = DefaultConnection(path_config_file)
    att_model = AttModel(conn.get_connection())
    att_reloj = AttReloj(conn.get_connection())
    cursor_att_reloj = att_reloj.get_cursor_reloj()
    att_model.create_tmp_table_att()

    for reloj in conn.get_result_to_dicts(cursor_att_reloj):
        print ("reloj {0}, ip {1}".format(reloj['nombre'], reloj['ip']))
        zk = zkt.ZKLib(reloj['ip'], 4370)
        zk_is_connect = zk.connect()
        print ("zk_is_connect", zk_is_connect)

        if zk_is_connect:

            attendance = zk.getAttendance()
            #print attendance
            list_att = []
            if attendance:
                for att in attendance:
                    list_att.append((att[0], att[2], reloj['nombre']))
                    att_model.insert_data_to_tmp_table_att(list_att)

                    if att_model.insert_diff_data_from_tmp_to_att():
                        #zk.clearAttendance()
                        zk.workCode()
                    else:
                        print("Fail to connect to ZK_ATT")
    conn.close_connection()

if __name__ == "__main__":
    collect_att_log(os.path.join(sys.path[0], "config.ini"))
