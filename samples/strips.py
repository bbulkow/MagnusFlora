#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs =512 
numChase = 4
chase_size = 4
gap_size = 3
frame_delay = 0.03

# strip0 = pixels 0-63
# strip1 = 64-127
# strip2 = 128-191
# etc. 

StripSize = 30

Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]
PINK=(150,50,50)
BLUE=(5,5,155)
GREEN=(5,155,5)

client = opc.Client('127.0.0.1:7890')

while True:
	for chase in range(StripSize):
		pixels = [ PINK ] * numLEDs 
	    	for base in Bases:
			for body in range(chase_size):
				green_dot = chase + body
				if green_dot < StripSize:
					pixels[base+green_dot] = GREEN
				blue_dot = chase + body + chase_size + gap_size
				if blue_dot < StripSize:
					pixels[base+blue_dot] = BLUE
		client.put_pixels(pixels)
		time.sleep(frame_delay)
