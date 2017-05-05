# global data that more than one thread needs to access
from ledlib import colordefs

pixels_per_fadecandy	= 512
number_fadecandy			=	4
total_pixels					=	pixels_per_fadecandy * number_fadecandy

basecolor							=	colordefs.colortable["DIM"]

all_the_pixels				=	[ basecolor ] * total_pixels

ledcontrol = ""



