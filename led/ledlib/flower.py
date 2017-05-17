# class definitions for the flower as a whole

# TODO: import from rest.portal

from ledlib.portal import Resonator, Portal
from ledlib.helpers import debugprint

from ledlib import patterns
from ledlib import colordefs


import threading
import logging
import time
# python3 calls it Queue
import queue

# LedPortal has LedResonators in the 'resos' object 

class LedPortal(Portal):

	valid_positions = [  "N", "NE", "E", "SE", "S", "SW","W", "NW" ]

	def __init__(self, log):

		Portal.__init__(self,id,log)

		log.debug(" LedPortal initializing !!! ")

		verbose=True

		# THIS IS EXAMPLE CODE
		self.title = "Dreamer Archetype"
		# initialize the resos - TODO should be from file
		for pos in Portal.valid_positions:
			vals = {'level': 4, 'health': 100, 'owner': "az" }
			r = Resonator(pos, log, vals)
			self.resonators[pos] = r

		self.faction = 1

		self.resos = {}
		for fc in range(4):								# 4 FAdecandy boards
			for side in range(2):						# 2 sets of 4 channels each
				reso_number = fc * 2 + side		# 8 resos
				reso_name = self.valid_positions[reso_number]
				self.resos[reso_name] = LedResonator(reso_number, reso_name, fc, side, 
								self.level, self.health, self.faction, log)

# Pixelstring
# name
# base
# size
# direction ( for motion? )

class PixelString(object):
	def __init__(self, name, base, size, direction):
		self.name = name
		self.base = base
		self.size = size
		self.direction = direction
		# TODO: validate direction = 1 or -1
		self.pixels = [0] * self.size
		# why didn't I just use reversed() ?
		if direction == 1:
			for i in range (size):
				self.pixels[i] = base + i
		if direction == -1:
			for i in range (size):
				self.pixels[i] = base + size -1 -i

# Input paramters:
#   'fadecandy', which is an integer which is the base pixel of the FC
#   side, which is either 0 or 1 ( side of the FC? )
#
# a base, which was the base of the fadecandy
# self.LOC - a PixelString of Left Outside
# self.CBOT
# self.LIC - left inner
# self.RIC - right inner center?
# self.RB
# self.
# list_of_lists_of_pixel_numbers - all the pixels in the petal

class PixelMap(object):

	def __init__(self, fadecandy, side):
		# TODO: validate side is 0 or 1
		self.base = (512 * fadecandy) + (256 * side)
		channels = [0, 64, 128, 192]		# TODO these should be in math
		# TODO: better way for overrides

		debugprint (("fadecandy ", fadecandy, "side ", side))

		cbase = self.base  + channels[0]
		self.LOC = PixelString ( "LOC", cbase, 43, 1)
		self.__CBOT = PixelString ("CBOT", cbase + 43, 21, -1)

		cbase = self.base + channels[1]
		self.LIC = PixelString ("LIC", cbase, 36, 1)
		self.LB = PixelString ( "LB", cbase+36, 28, 1)

		cbase = self.base + channels[2]
		self.RIC = PixelString ("RIC", cbase, 36, 1)
		self.RB = PixelString ( "RB", cbase+36, 28, -1)

		cbase = self.base + channels[3]
		self.ROC = PixelString ( "ROC", cbase, 43, 1)
		self.__CTOP = PixelString ("CTOP", cbase + 43, 21, -1)

		self.CENTER = PixelString("CENTER", 0, 42, 1)
		self.CENTER.pixels = self.__CBOT.pixels + self.__CTOP.pixels

		self.list_of_lists_of_pixel_numbers = [ \
			self.LOC.pixels, \
			self.LIC.pixels, \
			self.CENTER.pixels, \
			self.RIC.pixels, \
			self.ROC.pixels, \
			self.LB.pixels, \
			self.RB.pixels \
			]

		# "lixel" was originally a typo but it's a great unique tag
		debugprint (" Here comes the list of pixel numbers" )
		debugprint ((self.list_of_lists_of_pixel_numbers))
		debugprint (("Center: ", self.CENTER.pixels))
		debugprint (("LOC: ", self.LOC.pixels))
		debugprint (" Wheee!!!")

class PetalAction():
	def __init__(self):
		pass

# AKA a petal
# has a queue and a thread that reads the queue

class LedResonatorThread( threading.Thread):
	# todo: set more things
	def __init__(self,  ledResonator):
		threading.Thread.__init__(self)
		self.ledResonator = ledResonator
		self.logger = ledResonator.logger

	def run(self):
		q = self.ledResonator.queue
		reso = self.ledResonator # this is myself, for a shortcut
		while True:
			action = q.get()

			self.logger.debug( "LedResonator %s received action %s ",reso.position,action)
			
			if action == "INIT":
				debugprint((" resonator ", reso.position, " received action ",action))

				patterns.parallel_blend(reso.pixelmap.list_of_lists_of_pixel_numbers, \
						colordefs.colortable["ENL"], \
						colordefs.colortable["R4"], \
						4, \
						200)

			q.task_done() # tells other guy you are complete


class LedResonator(Resonator):


	# usage:
	# resos.append(Ledresonator(reso_number, reso_name, fc, side, level, health, faction)

	def __init__( self, reso_number, reso_name, fc, side, level, health, faction, log ):

		# superclass init
		Resonator.__init__(self, reso_name, log)

		self.pixelmap = PixelMap (fc, side)
		# run_pattern ("WAKEUP",
		#							self.pixelmap)

		# create the queue between this and the execution thread
		self.queue = queue.Queue()

		# may have to fix up argument so self gets to run
		r_thread = self.thread = LedResonatorThread(self)
		r_thread.start()

	def action(self,action):
		self.queue.put(action)




