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

StripSize = 30

Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]

client = opc.Client('127.0.0.1:7890')

pixels = [ colortable["MUTED_GRAY"] ]  * numLEDs 
for base in Bases:
	for resolevel in range(9):
		print ("Reso = ", resolevel)
		pixels [ base + gap_size + (resolevel*2) ] = RESO_COLORS[resolevel]
		pixels [ base + gap_size + (resolevel*2) +1 ] = RESO_COLORS[resolevel]
client.put_pixels(pixels)
client.put_pixels(pixels)

