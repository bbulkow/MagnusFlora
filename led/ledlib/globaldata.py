# global data that more than one thread needs to access
from ledlib import colordefs

pixels_per_fadecandy	= 512
number_fadecandy			=	4
total_pixels					=	pixels_per_fadecandy * number_fadecandy

basecolor							=	colordefs.colortable["DIM"]

all_the_pixels				=	[ basecolor ] * total_pixels

ledcontrol = ""

# I'm sure there is a universe where this is the proper place to put this function.
def setpixel(index,rgb):
	print ("Setting pixel %n to %s", index, rgb)
	try:
		all_the_pixels[index] = rgb
	except IndexError:
		return 1


