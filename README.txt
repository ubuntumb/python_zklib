# Python ZKLib #

ZK fingerprint Attendance Machine Library for python with a connection to the network using the UDP protocol and port 4370

# FORK FROM https://github.com/dnaextrim/python_zklib #
##Docs
See ZK communication protocol manual [here](https://github.com/vodvud/php_zklib/blob/master/zklib/docs/ZK_Communication_protocol_manual_CMD.pdf)
http://blog.infobytesec.com/2014/07/perverting-embedded-devices-zksoftware_2920.html?m=1

## Getting started

Login as admin to attendance machine and set the ip address for example (to 192.168.1.201) and connect the machine with ethernet to your network.
Edit zkconst.py to update database setting
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'dbname': 'test',
    'user': 'postgres',
    'password': '',
    'port': 5432
}
```
Create database for persist attendance data
```sql
CREATE DATABASE test
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

CREATE TABLE att
(
  pin character varying,
  marcacion timestamp without time zone,
  nombre character varying
)
;

CREATE TABLE reloj
(
  id bigserial NOT NULL,
  nombre character varying,
  ip character varying,
  CONSTRAINT pk_reloj PRIMARY KEY (id)
);
```
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
