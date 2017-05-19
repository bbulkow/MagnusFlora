# All the code needed to implement pattern masking
# only a subset of the clearest colors are used

from ledlib.helpers import debugprint, verboseprint
from ledlib import colordefs

# A mask is a list of colors and transparencies
# Simple Colors:
# kw				=	black, white
# roygbiv		=	basic colors  # might even simplfy this to wcmyk
# X					= Portal Faction
# R					=	RES
#	E					=	ENL
#	N					=	NEUTRAL
# -					=	completely transparent (i.e. non-masked)
# 0					= Passed color 0
# 1					=	Passed color 1 [...]

maskcolortable = {
	"R"	:	colordefs.colortable["RES"],
	"E"	:	colordefs.colortable["ENL"],
	"w"	:	colordefs.colortable["WHITISH"],
	"k"	:	colordefs.colortable["BLACKISH"],
	"-"	:	colordefs.colortable["NOTACOLOR"]
}

class MaskPos(object):
	def __init__(self, maskchar, opacity=1.00, rgb=[0,0,0]):
		self.opacity=opacity
		self.rgb = rgb
		if maskchar == "-":
			self.opacity = 0.00
			self.rgb = [0,0,0]
		elif maskchar == 0:
			pass
		elif maskchar == "N":
			self.rgb = colordefs.colortable["NEUTRAL"]
		elif maskchar in maskcolortable:
			self.rgb = maskcolortable[maskchar]
		else:
			self.opacity = 0.00
			self.rgb = [0,0,0]
			log.info (" bad or unimplemented mask  %s, using transparent", maskchar)

defaultmaskpos = MaskPos("-")

class Mask (object):
	def __init__(self,string,opacity=[1.00],
			rgbtable=[colordefs.colortable["NOTACOLOR"]]):
		# TODO: implement passed color(s)
		self.name = string
		self.size = len(string)
		self.opacity = [1.00] * self.size
		# TODO: implement variable (or even passed static) opacity
		debugprint (("Creating a mask from ", self.name))
		self.pos = [defaultmaskpos] * self.size
		for i in range(self.size):
			self.pos[i] = MaskPos(self.name[i], self.opacity[i])

	def apply(self, pixel_list):
		pixel_list_size = len(pixel_list)
		scope = min(pixel_list_size, self.size)
		result = [0,0,0] * scope			# dimension result list





