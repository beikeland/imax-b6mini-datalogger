#!/usr/bin/env python3
import time
import hid
import sys

#config
query_interval = 1
device = (0, 1)
###

h = hid.device()
h.open(device[0], device[1])

h.write([0x0F, 0x03, 0x55, 0x00, 0x55, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
h.read(64, 1000)

print ("state, energy, timer, voltage, current, ext temp, int temp, cell 1, cell 2, cell 3, cell 4, cell 5, cell 6")

t = time.clock()

while True:
	h.write([0])
	data = h.read(64, 1000)
	
	if (len(data) < 29):
		print("err")
		continue

	print(
		str(data[4]) + ", " +
		str(data[5] * 256 + data[6]) + ", " +
		str(data[7] * 256 + data[8]) + ", " +
		str((data[9] * 256 + data[10]) / 1000.0) + ", " +
		str((data[11] * 256 + data[12]) / 1000.0) + ", " +
		str(data[13]) + ", " +
		str(data[14]) + ", " +
		str((data[17] * 256 + data[18]) / 1000.0) + ", " +
		str((data[19] * 256 + data[20]) / 1000.0) + ", " +
		str((data[21] * 256 + data[22]) / 1000.0) + ", " +
		str((data[23] * 256 + data[24]) / 1000.0) + ", " +
		str((data[25] * 256 + data[26]) / 1000.0) + ", " +
		str((data[27] * 256 + data[28]) / 1000.0))
	sys.stdout.flush()
	
	time.sleep(query_interval - (time.clock() - t))
	t = time.clock()
