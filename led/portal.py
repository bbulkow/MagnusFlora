#!/usr/bin/env python3

# Control the LEDs of the Magnus Flora portal art display
import opc
import sys, argparse
from ledlib.colordefs import *
from ledlib.helpers import usage, debugprint, verboseprint
from ledlib.ledmath import *
from ledlib.flower import Ledportal
from ledlib import globalconfig
from ledlib import globaldata
from ledlib import patterns
from ledlib import heartbeat
from ledlib import colordefs

from ledlib.opcwrap import start_opc, ledwrite
from ledlib import opcwrap

from threading import Thread

def parse_command_line(argv):
	print ('Number of arguments:', len(sys.argv), 'arguments.')
	print ('Argument List:', str(sys.argv))

	desc = "Control the LED display.  Use @[filename] to read arguments from a file."

	parser = argparse.ArgumentParser(description=desc, \
						fromfile_prefix_chars='@')
	parser.add_argument('--color', type=check_COLOR, \
				help="Named color, can be overridden piecewise.")
	parser.add_argument('--red', type=check_RGB)
	parser.add_argument('--green', type=check_RGB)
	parser.add_argument('--blue', type=check_RGB)
	parser.add_argument('--debug', dest='debug', action='store_true')
	parser.add_argument('--nodebug', dest='debug', action='store_false')
	parser.add_argument('--verbose', dest='verbose', action='store_true')
	parser.add_argument('--noverbose', dest='verbose', action='store_false')
	parser.add_argument('--fastwake', dest='fastwake', action='store_true')
	parser.add_argument('--nofastwake', dest='fastwake', action='store_false')
	commandline = parser.parse_args()
	return commandline

def setup(argv):

	commandline = parse_command_line(argv)

	# command line flags
	globalconfig.debugflag = commandline.debug
	globalconfig.verboseflag = commandline.verbose
	globalconfig.fastwake = commandline.fastwake

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
	verboseprint ("Let there be light!")

	# Wake up the whole portal
	patterns.wake_up (0, globaldata.total_pixels, globaldata.basecolor)

	# start a simple thread for asynchronous heartbeat
	EKG = Thread(target=heartbeat.ticktock)
	EKG.start()
	verboseprint ("Global heartbeat started.")

	ledportal = Ledportal()

# def parallel_fade (list_of_lists_of_pixel_numbers, \
#      rgb_color_triplet, fade_ratio=0.5, speed=0, steps=100):

	patterns.parallel_fade(ledportal.resos[0].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["R4"], \
			0.2, \
			3, \
			200)

	# start one thread for each resonator to listen for changes

	verboseprint ("Ready for commands.")

if __name__ == "__main__":
   main(sys.argv[1:])
