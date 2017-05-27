#!/usr/bin/env python3
""" Exercise library functions on the leds of a single petal."""

# Not even pretending to be production code, this program lets you run
# some patterns from the production libraries on a single petal.

# Control the LEDs of the Magnus Flora portal art display
import opc
import sys, argparse
from ledlib.colordefs import *
from ledlib.helpers import usage, debugprint, verboseprint
from ledlib.ledmath import *
from ledlib.flower import LedPortal
from ledlib import globalconfig
from ledlib import globaldata
from ledlib import patterns
from ledlib import heartbeat
from ledlib import colordefs
from ledlib import portalconfig			# base/demo state of portal
from ledlib import patterns

from ledlib.opcwrap import start_opc, ledwrite
from ledlib import opcwrap

##### ----------------------------
import riggeddemo
##### ----------------------------

import ledportal							# so I can steal the logging code


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
	parser.add_argument('--noop', dest='noop', action='store_true')
	parser.add_argument('--fastwake', dest='fastwake', action='store_true')
	parser.add_argument('--nofastwake', dest='fastwake', action='store_false')
	parser.add_argument('--north', dest='north', type=check_RESO,
					help="From 0 to 7, which reso is north?")
	parser.add_argument('--pattern', dest='pattern', type=patterns.check_PATTERN,
					help="Name of defined pattern, such as CHASE or TEST")
	parser.add_argument('--level', dest='level', type=int,
					help="Starting Level of sample petal.")
	parser.add_argument('--faction', dest='faction', type=colordefs.faction_rgb,
					help="RES/ENL/NEUTRAL - rgb is what is stored")
	commandline = parser.parse_args()
	return commandline

def setup(argv):

	commandline = parse_command_line(argv)

	# command line flags
	globalconfig.debugflag = commandline.debug
	globalconfig.verboseflag = commandline.verbose
	globalconfig.fastwake = commandline.fastwake
	globalconfig.noop			=	commandline.noop
	portalconfig.north		= commandline.north
	portalconfig.pattern	=	commandline.pattern
	riggeddemo.level = commandline.level
	riggeddemo.factionrgb = commandline.faction

	# logging
	globalconfig.log = ledportal.create_log(commandline)

	if globalconfig.noop:
		print ("No-op mode.  Pixels will not fire.")
		debugprint ("No-op mode.  Pixels will not fire.")

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

	# ledportal = LedPortal( None, log )

	# print ("writing ", finalcolor, " to the LEDs.")
	# pixels = [ finalcolor ] * numLEDs

	# ledwrite (ledcontrol, pixels)

	return

def main(argv):

	ledportal.setup(argv)

	# start a simple thread to asynchronously push the pixel array to the LEDs
	let_there_be_light = Thread(target=opcwrap.ledwriteloop)
	let_there_be_light.start()
	verboseprint ("Let there be light!")

	# Wake up the whole portal
	patterns.wake_up (0, globaldata.total_pixels, globaldata.basecolor)
	verboseprint ("... and there was light.")

	# start a simple thread for asynchronous heartbeat
	EKG = Thread(target=heartbeat.ticktock)
	EKG.start()
	verboseprint ("Global heartbeat started.")

	thisledportal = LedPortal( None, globalconfig.log)
	level = riggeddemo.level


# def parallel_fade (list_of_lists_of_pixel_numbers, \
#      rgb_color_triplet, fade_ratio=0.5, speed=0, steps=100):

	# this is the base for one type of pattern. Steal the pixel data
	# and feed it to the subthreads as static.

# 	patterns.parallel_blend(thisledportal.resos[0].pixelmap.list_of_lists_of_pixel_numbers, \
# 			colordefs.colortable["ENL"], \
# 			colordefs.colortable[colordefs.RESO_COLOR_NAMES[level]], \
# 			4, \
# 			200)
# 

# Normally patterns are invoked in parallel through the threads running inside each reso object.

	if True:
		patterns.parallel_blend(thisledportal.resos["E"].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["ENL"], \
			colordefs.colortable[colordefs.RESO_COLOR_NAMES[3]], \
			4, \
			200)

	if False:
		patterns.parallel_blend(thisledportal.resos["SE"].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["ENL"], \
			colordefs.colortable[colordefs.RESO_COLOR_NAMES[8]], \
			4, \
			200)

	if False:
		patterns.parallel_blend(thisledportal.resos["S"].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["ENL"], \
			colordefs.colortable[colordefs.RESO_COLOR_NAMES[7]], \
			4, \
			200)

	if False:
		patterns.parallel_blend(thisledportal.resos["SW"].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["ENL"], \
			colordefs.colortable[colordefs.RESO_COLOR_NAMES[3]], \
			4, \
			200)

	if True:
		patterns.parallel_blend(thisledportal.resos["NE"].pixelmap.list_of_lists_of_pixel_numbers, \
			colordefs.colortable["ENL"], \
			colordefs.colortable[colordefs.RESO_COLOR_NAMES[level]], \
			4, \
			200)

	patterns.chase(thisledportal.resos["NE"].pixelmap.list_of_lists_of_pixel_numbers, \
		"ww--ww--ww", -1, thisledportal.resos["SE"])


# Not needed -- init of a reso starts the thread.
	# start one thread for each resonator and mod to listen for changes
	# resothreads = [""] * 8
	# modthreads	=	[""] * 4

	# for

	# verboseprint ("Ready for commands.")

if __name__ == "__main__":
   main(sys.argv[1:])
