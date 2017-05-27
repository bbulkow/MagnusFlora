#!/usr/bin/env python3

# Control the LEDs of the Magnus Flora portal art display
import opc
import sys, argparse, logging
from ledlib.helpers import usage, debugprint, verboseprint
from ledlib.ledmath import *
from ledlib.flower import LedPortal, LedAction
from ledlib import globalconfig
from ledlib import globaldata

from ledlib import heartbeat

from ledlib.colordefs import *
from ledlib import portalconfig					# base/demo state of portal
from ledlib import patterns
#from ledlib import colordefs
#from ledlib import patterns

from ledlib.opcwrap import start_opc, ledwrite
from ledlib import opcwrap

from ledlib.portal import Resonator, Portal

from threading import Thread
import time

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

	parser.add_argument('--debuglevel', '-d', help=" debug level: CRITICAL ERROR WARNING INFO DEBUG", default="DEBUG", type=str)
	parser.add_argument('--log', help="location of the log file", default="ledlib.log", type=str)

	commandline = parser.parse_args()
	return commandline

def setup(argv):

	commandline = parse_command_line(argv)

	log = create_log(commandline)

	# command line flags
	globalconfig.debugflag = commandline.debug
	globalconfig.verboseflag = commandline.verbose
	globalconfig.fastwake = commandline.fastwake
	globalconfig.noop			=	commandline.noop
	globalconfig.log = log
	portalconfig.north		= commandline.north
	portalconfig.pattern	=	commandline.pattern

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

	# ledportal = LedPortal( None, log)

	# print ("writing ", finalcolor, " to the LEDs.")
	# pixels = [ finalcolor ] * numLEDs

	# ledwrite (ledcontrol, pixels)

	return

def create_log(args):
    # create a logging object and add it to the app object
    log = logging.getLogger('MF_LEDLIB')
    log.setLevel(args.debuglevel)
    # create a file output
    fh = logging.FileHandler(args.log)
    fh.setLevel(args.debug)
    # create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(args.debug)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log

def main(argv):

	setup (argv)
	log = globalconfig.log

	# start a simple thread to asynchronously push the pixel array to the LEDs
	let_there_be_light = Thread(target=opcwrap.ledwriteloop)
	let_there_be_light.start()
	log.debug ("Let there be light!")

	# Wake up the whole portal - can take a long time unless fastwake
	patterns.wake_up (0, globaldata.total_pixels, globaldata.basecolor)
	log.debug ("... and there was light.")

	# start a simple thread for asynchronous heartbeat
	EKG = Thread(target=heartbeat.ticktock)
	EKG.start()
	verboseprint ("Global heartbeat started.")

	# create the LedPortal object - fundamental init
	ledportal = LedPortal(None, globalconfig.log )

# def parallel_fade (list_of_lists_of_pixel_numbers, \
#      rgb_color_triplet, fade_ratio=0.5, speed=0, steps=100):

	# TODO: A test initialization. Move this within the LedPortal code
	# first color=stem, second color=edge
#	for r in Resonator.valid_positions:
#		patterns.parallel_blend(ledportal.resos[r].pixelmap.list_of_lists_of_pixel_numbers, \
#				colordefs.colortable["ENL"], \
#				colordefs.colortable["R4"], \
#				4, \
#				200)

	# send the init action to all the petals
	# this is now ASYNC so you should see all work together
	a = LedAction('INIT')
	for r in Resonator.valid_positions:
		ledportal.resos[r].do_action(a)

	log.info ("Ready for commands.")

	# some test code - a 
	log.info ("sleeping 5 seconds")
	time.sleep(5.0)

	log.info(" generating attack by ENL")
	a = LedAction('ATTACK', 2)
	for r in Resonator.valid_positions:
		ledportal.resos[r].do_action(a)

	time.sleep(8.0)
	log.info(" generating attack by RES")

	a = LedAction('ATTACK', 1)
	for r in Resonator.valid_positions:
		ledportal.resos[r].do_action(a)

	time.sleep(100.0)

if __name__ == "__main__":
   main(sys.argv[1:])
