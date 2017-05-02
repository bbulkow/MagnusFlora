# class definitions for the flower as a whole

from flask.portal import Resonator, Portal

class Ledportal(Portal):

	def __init__(self):
		verbose=True
		Portal.__init__(self,id,verbose)
		self.title = "Dreamer Archetype"

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

class Ledresonator(Resonator):

	def __init__(self, pixelmap):
		Resonator.__init__(self)

