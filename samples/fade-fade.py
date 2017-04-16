#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import sys
if sys.version_info[0] < 3:
	raise "Must be using python3"

import opc, time
import argparse

# todo: add arg
numLEDs = 36

def fade_cycle(client, color, duration, delay, step ):
	global numLEDs
	start_time = time.time()
	pixel_value = 0
	while True:

		#print (" Pixel value ",pixel_value)
		if (color=="r"):
			pixel = (pixel_value, 0, 0 )
		elif (color=="g"):
			pixel = (0, pixel_value, 0 )
		elif (color=="b"):
			pixel = (0, 0, pixel_value )
		else:
			pixel = (pixel_value, pixel_value, pixel_value)
	
		pixels = [ pixel ] * numLEDs
		if not client.put_pixels(pixels):
			print(" fade cycle: no longer connected, retrying")
			return False

		pixel_value += step	
		if pixel_value > 255:
			pixel_value = 0

		if time.time() > start_time + duration:
			return
	
		time.sleep(delay)

# Returns a valid client connection object
def opc_connect(opc_host):
	while True:

		client = opc.Client(opc_host)
		if client.can_connect():
			print( " opc connected ")
			return(client)
		else:
			print("not connected trying again")
		time.sleep(1.0)

	
parser = argparse.ArgumentParser(description="Quick Tester For LEDs")
parser.add_argument('--opc', help="OPC connection string", default="localhost:7890", type=str)
parser.add_argument('--color', help="w , r , g , b; fades through that color", default="w", type=str)
parser.add_argument('--delay', help="delay between steps in float seconds", default=0.1, type=float)
parser.add_argument('--duration', help="number of seconds to run excluding network problems", default=999999, type=int)
parser.add_argument('--step', help="decimal amount to increase color by per cycle", default=10, type=int)
args = parser.parse_args()
print(" starting LED test against OPC at ",args.opc," color ",args.color," delay ",args.delay," step ",args.step)

valid_colors = ["w", "r", "g", "b"]
if args.color not in valid_colors:
	print(" color must be one of r,g,b,w, instead is ",args.color)
	raise "invalid input"

start_time = time.time()
while True:
	client = opc_connect(args.opc)
	fade_cycle(client, args.color, args.duration, args.delay, args.step)
	if time.time() > start_time + args.duration:
		break;



