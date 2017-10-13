#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
from ledlib.colordefs import *

#numLEDs =1024*64 
numChase = 4
chase_size = 4
gap_size = 3
frame_delay = 0.04
numStrips = 32
numLEDs =numStrips*64 

# strip0 = pixels 0-63
# strip1 = 64-127
# strip2 = 128-191
# etc. 

StripSize = 64  

#Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]
#Bases = [ 512, 576, 650, 704, 768, 832, 896, 960 ]

client = opc.Client('127.0.0.1:7890')

Bases = []
for stripIdx in range(numStrips):
    Bases.append(stripIdx*64)
print (Bases)

#print("len pixels is ", len(pixels))

while True:
    for resolevel in range(9):
        for chase in range(StripSize):
            pixels = [ colortable["DIM"] ] * numLEDs 
            for base in Bases:
                for body in range(chase_size):
                    pixel_dot = chase + body
                    if pixel_dot < StripSize:
                        pixels[base+pixel_dot] = RESO_COLORS[resolevel]
            client.put_pixels(pixels)
            time.sleep(frame_delay)
