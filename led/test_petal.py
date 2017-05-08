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

StripSize = 64
NumStrips = 8

Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]
PINK=(150,50,50)
BLUE=(5,5,155)
GREEN=(5,155,5)

# Yes a dict would have been better.
TEST_WHITE		= ((200,200,200), "almost white")
TEST_RED			=	((200,0,0), "red")
TEST_ORANGE	=	((170,120,20), "orange")
TEST_YELLOW	=	((200,200,80), "yellow")
TEST_GREEN		=	((20,180,20), "green")
TEST_BLUE		=	((20,20,180),	"blue")
TEST_PURPLE	=	((70,0,130),	"purple")
TEST_BLACK		=	((20,20,20), "blackish")

# test_colors = [ TEST_WHITE[0], TEST_RED[0], TEST_ORANGE[0],
# 								TEST_YELLOW[0], TEST_GREEN[0],
# 								TEST_BLUE[0], TEST_PURPLE[0], TEST_BLACK[0] ]

test_colors = [ TEST_WHITE, TEST_RED, TEST_ORANGE,
								TEST_YELLOW, TEST_GREEN,
								TEST_BLUE, TEST_PURPLE, TEST_BLACK ]

for i in range(NumStrips):
	print ("Channel: "+ str(i)+ " color: "+ test_colors[i][1])

print ("""
Petal config:
	Even petal:
		Left Outer Curve: white
		Left inner curve: red
		Center: yellow on top, white on bottom (long connector)
		Right inner curve: orange
		Right outer curve: yellow
		Back/Top  left: red
		Back/Top right:	orange

	Odd petal:
		Left Outer Curve: green
		Left inner curve: blue
		Center: blackish on top, green on bottom (long connector)
		Right inner curve: purple
		Right outer curve: blackish
		Back/Top  left: blue
		Back/Top right:	purple

	If things don't match up, remember to power down before swapping!
""")

client = opc.Client('127.0.0.1:7890')

while True:
	for chase in range(StripSize):
		pixels = [ PINK ] * numLEDs
		for i in range(NumStrips):
			base = Bases[i]
			basecolor = test_colors[i][0]
			for j in range(StripSize):
				pixels [base+j] = basecolor
			for body in range(chase_size):
				green_dot = chase + body
				if green_dot < StripSize:
					pixels[base+green_dot] = GREEN
				blue_dot = chase + body + chase_size + gap_size
				if blue_dot < StripSize:
					pixels[base+blue_dot] = BLUE
		client.put_pixels(pixels)
		time.sleep(frame_delay)
