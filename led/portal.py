#!/usr/bin/env python3

# Control the LEDs of the Magnus Flora portal art display
import opc
import sys, argparse
from ledlib.colordefs import *
from ledlib.helpers import usage, debugprint
from ledlib.ledmath import *
from ledlib.flower import Ledportal
from ledlib import globalconfig
from ledlib import globaldata
from ledlib import patterns

from ledlib.opcwrap import start_opc, ledwrite
from ledlib import opcwrap

from threading import Thread

def parse_command_line(argv):
	print ('Number of arguments:', len(sys.argv), 'arguments.')
	print ('Argument List:', str(sys.argv))

	parser = argparse.ArgumentParser(description='Solid colors on LED strip.')
	parser.add_argument('--red', type=check_RGB)
	parser.add_argument('--green', type=check_RGB)
	parser.add_argument('--blue', type=check_RGB)
	parser.add_argument('--color', type=check_COLOR)
	commandline = parser.parse_args()
	return commandline

def setup(argv):

	globalconfig.debugflag = True		# TODO: command line
	commandline = parse_command_line(argv)

	# specified RGB values override named colors
	if hasattr(commandline, 'color'):
		try:
			basecolor = colortable[commandline.color]
		except KeyError:
			basecolor = colortable["MUTED_PINK"]
			basecolor = colortable["DIM"]
	debugprint ("Base color 0 is ")
	debugprint (basecolor)

	if hasattr(commandline, 'red') and commandline.red:
		red = commandline.red
	else:
		red = basecolor[0]

	if hasattr(commandline, 'green') and commandline.green:
		green = commandline.green
	else:
		green = basecolor[1]

	if hasattr(commandline, 'blue') and commandline.blue:
		blue = commandline.blue
	else:
		blue = basecolor[2]

# 	if hasattr(commandline, 'red'):
# 		try:
# 			red = commandline.red
# 		except TypeError:
# 			red = basecolor[0]
# 

	globaldata.basecolor = (red, green, blue)

	globaldata.ledcontrol = start_opc()

	# ledportal = Ledportal()

	# print ("writing ", finalcolor, " to the LEDs.")
	# pixels = [ finalcolor ] * numLEDs

	# ledwrite (ledcontrol, pixels)

	return

def main(argv):

	setup (argv)

	# start a simple thread to asynchronously push the pixel array to the LEDs
	let_there_be_light = Thread(target=opcwrap.ledwriteloop)
	let_there_be_light.start()

	# Wake up the whole portal
	patterns.wake_up (0, globaldata.total_pixels, globaldata.basecolor)

if __name__ == "__main__":
   main(sys.argv[1:])
