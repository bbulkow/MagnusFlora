#!/usr/bin/env python3

# flash all the pixels on a Fadecandy to the same color
import opc
import sys, argparse
from ledlib.colordefs import *
from ledlib.helpers import usage


def main(argv):

	server="127.0.0.1"
	port="7890"


  # these need to go in a library
	numLEDs = 512
	StripSize = 30
	Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]

	COLOR = MUTED_GRAY

	print ('Number of arguments:', len(sys.argv), 'arguments.')
	print ('Argument List:', str(sys.argv))

	parser = argparse.ArgumentParser(description='Solid colors on LED strip.')
	parser.add_argument('--red', default='20', type=int)
	parser.add_argument('--green', default='20', type=int)
	parser.add_argument('--blue', default='20', type=int)
	commandline = parser.parse_args()
	
	client_home = "".join([server,":",port])
	print ("opening opc on ", client_home)
	client = opc.Client(client_home)

	COLOR = (commandline.red, commandline.green, commandline.blue)
	print ("writing ", COLOR, " to the LEDs.")
	pixels = [ COLOR ] * numLEDs
	client.put_pixels(pixels)


if __name__ == "__main__":
   main(sys.argv[1:])
