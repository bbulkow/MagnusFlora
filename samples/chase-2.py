#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from itertools import cycle

numLEDs = 24
numChase = 4
client = opc.Client('192.168.4.15:7890')

while True:
	for i in range(numLEDs):
		pixels = [ (150,50,50) ] * numLEDs
		# pixels[i] = (5, 5, 155)
		# pool = cycle(pixels)
		for j in range(numChase):
			if i+j <= numLEDs:
 				pixels[i+j-1] = (5, 5, 155)
		client.put_pixels(pixels)
		time.sleep(0.03)
