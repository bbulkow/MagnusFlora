#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from itertools import cycle

numLEDs = 512
numChase = 4
client = opc.Client('127.0.0.1:7890')

for i in range(numLEDs):
	pixels = [ (0,0,0) ] * numLEDs
	client.put_pixels(pixels)
