# class definitions for the flower as a whole

from flask.portal import Resonator, Portal
from ledlib.helpers import debugprint

class Ledportal(Portal):

	def __init__(self):
		verbose=True
		Portal.__init__(self,id,verbose)
		self.title = "Dreamer Archetype"
		# initialize the resos
		self.faction = "ENL"										# or flip a coin.
		self.level = 4
		self.health = 100
		self.resos = []
		for fc in range(4):								# 4 FAdecandy boards
			for side in range(2):						# 2 sets of 4 channels each
				reso_number = fc * 2 + side		# 8 resos
				reso_name = self.valid_positions[reso_number]
				self.resos.append(Ledresonator(reso_number, reso_name, fc, side, \
								self.level, self.health, self.faction))

class Pixelstring(object):
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

class Pixelmap(object):

	def __init__(self, fadecandy, side):
		# TODO: validate side is 0 or 1
		self.base = (512 * fadecandy) + (256 * side)
		channels = [0, 64, 128, 192]		# TODO these should be in math
		# TODO: better way for overrides

		debugprint (("fadecandy ", fadecandy, "side ", side))

		cbase = self.base  + channels[0]
		self.LOC = Pixelstring ( "LOC", cbase, 43, 1)
		self.CBOT = Pixelstring ("CBOT", cbase + 43, 21, -1)

		cbase = self.base + channels[1]
		self.LIC = Pixelstring ("LIC", cbase, 36, 1)
		self.LB = Pixelstring ( "LB", cbase+36, 28, 1)

		cbase = self.base + channels[2]
		self.RIC = Pixelstring ("RIC", cbase, 36, 1)
		self.RB = Pixelstring ( "RB", cbase+36, 28, -1)

		cbase = self.base + channels[3]
		self.ROC = Pixelstring ( "ROC", cbase, 43, 1)
		self.CTOP = Pixelstring ("CTOP", cbase + 43, 21, -1)

		self.CENTER = Pixelstring("CENTER", 0, 42, 1)
		self.CENTER.pixels = self.CBOT.pixels + self.CTOP.pixels

		self.list_of_lists_of_pixel_numbers = [ \
			self.LOC.pixels, \
			self.LIC.pixels, \
			self.CENTER.pixels, \
			self.RIC.pixels, \
			self.ROC.pixels, \
			self.LB.pixels, \
			self.RB.pixels \
			]

		debugprint (" Here comes the lixel numbers" )
		debugprint ((self.list_of_lists_of_pixel_numbers))
		debugprint (" Wheee!!!")

class Ledresonator(Resonator):

	# usage:
	# resos.append(Ledresonator(reso_number, reso_name, fc, side, level, health, faction)

	def __init__(self, \
							reso_number, \
							reso_name, \
							fc, side, \
							level, health, faction):
		Resonator.__init__(self, reso_name)
		self.pixelmap = Pixelmap (fc, side)
		# run_pattern ("WAKEUP",
		#							self.pixelmap)

