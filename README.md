# imax-b6mini-datalogger
Script for dumping data from IMAX B6 mini charger into `csv` format.

Usage: pipe stdout into file, if necessary run from root. Query interval and device VID/PID can be modified in script.

Requires https://pypi.python.org/pypi/hidapi/

Not tested with Windows, but it should work.

Forking to use with B6AC v2 (pr comments by alexwlpr) and adding ability to control charge/discharge/storage cycle. F.ex. charge and discharge 3 cycles and then apply storage charge.

Current progress of protocol decoding
```
#0f:16:05:00:01:01:02:07:d0:07:d0:0c:1c:10:04:00:00:00:00:00:00:00:00:f3:ff:ff + 00 ... 00
#           |  |  |  |     |     |     |                             |xx CheckSum8 Modulo 256 (skip first 2 bytes!)
#           |  |  |  |     |     |     |10:04 = 4100 mV charge voltage 16 bit mV
#           |  |  |  |     |     |0c:1c = 3100 mV discharge voltage 16 bit mV
#           |  |  |  |     |07:d0 = 2000mA discharge current 16 bit mA
#           |  |  |  |07:d0 = 2000mA charge current 16 bit mA
#           |  |  |xx 00=charge, 01=discharge, 02=storage ... cycle, fast charge, etc?
#           |  |xx = # cells 01..06.    
#           |xx cell type. 00=lipo, 01=lion, 02=life, 03=lihv, 04=nimh, 05=nicd, 06=pb
```

```
#DISCLAIMER. Python is _not_ my native language. 
#Only tested singe cell lithium ion cell - use at your own risk
from struct import *
LIPO = 0
LION = 1
LIFE = 2
LIHV = 3
NIMH = 4
NICD = 5
PB = 6
CHARGE = 0
DISCHARGE = 1
STORAGE = 2
S1=1
S2=2
S3=3
S4=4
S5=5
S6=6
POLL=0x55
STOP=0xFE

def packstrbuff(operation, celltype=None, cellcount=None, chargecurrent=None, dischargecurrent=None, dischargecutoff=None, chargecutoff=None):
	#pack binary string into data packet
	if celltype is not None and chargecutoff is not None:
		strbuff = pack(">H3b4H8x", 0x0500, celltype, cellcount, operation, ((6000, chargecurrent)[chargecurrent < 6000]), ((2000, dischargecurrent)[dischargecurrent < 2000]), dischargecutoff, chargecutoff)
		strbuff = pack(">xH", 0x0F16) + strbuff + pack(">BH37x", sum(map(ord, strbuff))%256, 0xFFFF) #add checksum and padding
	#or into a short control packet
	else:
		strbuff = pack(">xHBxBH56x", 0x0F03, operation, operation, 0xFFFF)		 #cheksum = operation byte it seems?
	#then convert string to list of integers - must be a better way?!
	listbuff = []
	for c in strbuff:
		listbuff.append(ord(c))
	return listbuff
  
h.write(packBuffer(CHARGE, LION, S1, 1000, 1000, 3100, 4100))
h.write(packBuffer(POLL))

```
