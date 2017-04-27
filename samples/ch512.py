#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from itertools import cycle

numLEDs =512 
numChase = 4

PINK=(150,50,50)
BLUE=(5,5,155)
GREEN=(5,155,5)

client = opc.Client('127.0.0.1:7890')

while True:
	for i in range(numLEDs):
		pixels = [ PINK ] * numLEDs
		# pixels[i] = (5, 5, 155)
		# pool = cycle(pixels)
		for j in range(numChase):
			if i+j <= numLEDs:
 				pixels[i+j-1] = BLUE
			if i+j+10 <= numLEDs:
				pixels[i+j+9] = GREEN
		client.put_pixels(pixels)
		time.sleep(0.03)
