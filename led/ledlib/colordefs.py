# Define various colors used by the LED strips
#
# Entry points:
#		function faction_rgb	returns (r,g,b)
#		dict colortable				entries string: (r,g,b)

colortable={}

colortable["MUTED_PINK"]	= (150,50,50)					# test color Joey liked
colortable["AZALEA"]			= (140,20,100)				# a/k/a "Aliza Pink"
colortable["HOTPINK"]			= (255,55,180)				# my eyes hurt
colortable["MUTED_GRAY"]	= (20,20,20)
colortable["SUNSHINE"]		= (100,100,20)				# visible in daylight
colortable["DIM"]					= (16,16,16)					# dimmest with no flicker

# Ingress-specific colors

# Faction colors were created randomly but I liked them.
# BLUE_RES = (5,5,155)		# pretty but has a slight flicker
# GREEN_ENL = (5,155,5)		# ""
BLUE_RES = (16,16,155)
GREEN_ENL = (16,155,16)
GRAY_NEUTRAL = (32,32,32)

NOTACOLOR		=	(-1,-1,-1)
colortable["NOTACOLOR"] = NOTACOLOR

RES = BLUE_RES
ENL = GREEN_ENL
NEUTRAL = GRAY_NEUTRAL

FACTION_COLORS = [ RES, ENL ]

def faction_rgb(faction):
	if faction == "RES":
		return colortable["RES"]
	if faction == "ENL":
		return colortable["ENL"]
	if faction == "NEUTRAL":
		return colortable["NEUTRAL"]
	else:
		debugprint (("faction_rgb: Undefined faction: ",faction))
		return colortable["NOTACOLOR"]


colortable["RES"] = RES
colortable["ENL"] = ENL
colortable["NEUTRAL"] = NEUTRAL

# also index by integer, which is commonly used elsewhere - use the same 0,1,2 system
colortable_faction = [ NEUTRAL, ENL, RES ]

# Level colors from IITC source, http://iitc.me
# Conversions via https://toolstud.io/color/rgb.php?rgbhex=9627F4
# Adjustments done by eye

# PURPLE_R8 = (150,39,244)	# 9627F4
PURPLE_R8 = (70,0,130)			# empirical
# VIOLET_R7 = (193,36,224)	# C124E0
VIOLET_R7 = (90,0,120)			# empirical
MAGENTA_R6 = (235,38,205)		# EB26CD
FUCHSIA_R5 = (253,41,146)	# FD2992
RED_R4 = (228,0,0)				# E40000
ORANGE_R3 = (255,115,21)	# FF7315
KUMQUAT_R2 = (255,166,48)	# FFA630
YELLOW_R1 = (254,206,90)	# FECE5A
EMPTY_RESO = (50,50,50)		# dim white

# I like the names above but they are impractical.

R0 = EMPTY_RESO
R1 = YELLOW_R1
R2 = KUMQUAT_R2
R3 = ORANGE_R3
R4 = RED_R4
R5 = FUCHSIA_R5
R6 = MAGENTA_R6
R7 = VIOLET_R7
R8 = PURPLE_R8

# The counting shall start at zero.
RESO_COLORS = [ R0, R1, R2, R3, R4, R5, R6, R7, R8 ]
RESO_COLOR_NAMES = ["R0","R1","R2","R3","R4","R5","R6","R7","R8"]

colortable["R0"] = R0
colortable["R1"] = R1
colortable["R2"] = R2
colortable["R3"] = R3
colortable["R4"] = R4
colortable["R5"] = R5
colortable["R6"] = R6
colortable["R7"] = R7
colortable["R8"] = R8

# also create an integer indexed table for levels
colortable_level = [ R0, R1, R2, R3, R4, R5, R6, R7, R8 ]

TEST_WHITE    = ((200,200,200), "almost white")
TEST_RED      = ((200,0,0), "red")
TEST_ORANGE = ((170,120,20), "orange")
TEST_YELLOW = ((200,200,80), "yellow")
TEST_GREEN    = ((20,180,20), "green")
TEST_BLUE   = ((20,20,180), "blue")
TEST_PURPLE = ((70,0,130),  "purple")
TEST_BLACK    = ((20,20,20), "blackish")

colortable["WHITISH"]		=	TEST_WHITE
colortable["BLACKISH"]	=	TEST_BLACK

