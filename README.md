# Python ZKLib #

ZK fingerprint Attendance Machine Library for python with a connection to the network using the UDP protocol and port 4370
# FORK FROM https://github.com/dnaextrim/python_zklib #
##Now
Python version 3.x supported

## Getting started

Login as admin to attendance machine and set the ip address for example (to 192.168.1.201) and connect the machine with ethernet to your network.

Connect to the machine

```python
import os
import sys
sys.path.append("zktlib")

from zktlib import zklib as zkt
import time
from datetime import datetime
import zkconst

zk = zkt.ZKLib("192.168.1.201", 4370)
ret = zk.connect()
print ("connection:", ret)
```
If result was
```
connection True
```
Then you are connected.

More examples on how to use the Library available in the
zkmain.py and zktest.py file
