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
	"R"	:	colordefs.
}

class Mask (object):
	def __init__(self,string,opacity=[1.00],
			rgbtable=[colordefs.colortable["NOTACOLOR"]]):
		self.name = string
		self.size = len(string)
		self.opacity = [1.00] * self.size
		debugprint (("Creating a mask from ", self.name))

