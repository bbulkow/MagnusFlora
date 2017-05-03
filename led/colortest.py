#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from ledlib.colordefs import *

numLEDs =512 
numChase = 4
chase_size = 4
gap_size = 3
frame_delay = 0.04

# strip0 = pixels 0-63
# strip1 = 64-127
# strip2 = 128-191
# etc. 

StripSize = 64	

Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]

client = opc.Client('127.0.0.1:7890')

while True:
	for resolevel in range(9):
		print ("Reso = ", resolevel)
		for chase in range(StripSize):
			pixels = [ MUTED_GRAY ] * numLEDs 
	    		for base in Bases:
				for body in range(chase_size):
					pixel_dot = chase + body
					if pixel_dot < StripSize:
						pixels[base+pixel_dot] = RESO_COLORS[resolevel]
			client.put_pixels(pixels)
			time.sleep(frame_delay)
