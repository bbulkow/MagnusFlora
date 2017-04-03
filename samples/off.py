#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from itertools import cycle

numLEDs = 24
numChase = 4
client = opc.Client('192.168.4.15:7890')

for i in range(numLEDs):
	pixels = [ (0,0,0) ] * numLEDs
	client.put_pixels(pixels)
