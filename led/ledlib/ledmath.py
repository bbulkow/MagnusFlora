# ledmath.py

from ledlib import globalconfig

RGB_min = 16		# below this we get flicker.  Disallow or use Fadecandy dither
RGB_max = 255		# as per spec
RGB_range = RGB_max - RGB_min

# values needed for single-strip testing
numLEDs = 512
StripSize = 30

# first pixel on each Fadecandy port - yeah, this is mathable.
Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]

def pixel_list (Fadecandy, strand, chunk, chunksize=30, direction=0):
	# given a defined chunk of LEDs, return a list of pixel numbers from
	# basewards to tipwards
	#
	from ledlib.helpers import debugprint, usage
  # sanity check
	if Fadecandy >= 10:
		usage ("Fadecandy value out of range: " + str(Fadecandy))
	if strand >= 8:
		usage ("strand value out of range: " + str(strand))
	if chunk >= 5:
		usage ("chunk value out of range: " + str(chunk))
	if chunksize > 64:
		usage ("chunksize value out of range: " + str(chunksize))
	if direction > 1:
		usage ("direction is 0 for normal, 1 for inverted")

	chunkhead = \
		512 * Fadecandy + \
		Bases [strand] + \
		chunk * chunksize
	chunktail = \
		chunkhead + chunksize

	debugprint ("head = "+str(chunkhead))
	debugprint ("tail = "+str(chunktail))
	# print ("head = "+str(chunkhead))
	# print ("tail = "+str(chunktail))

	pixels = [0] * chunksize
	for i in range (chunksize):
		if direction == 0:
			pixels[i] = chunkhead + i
		if direction == 1:
			pixels[i] = chunktail - i

	return pixels

def wrap():
	# function to put a pattern on a set of LEDs, possibly wrapping around
	# from the start point.
  pass


def check_RGB(value):
	# http://stackoverflow.com/questions/14117415
	cvalue = int(value)
	if (cvalue < 0) or (cvalue > 255):
		raise argparse.ArgumentTypeError("RGB values must be between 0 and 255")
	if (cvalue < RGB_min) and (cvalue > 0):
		raise argparse.ArgumentTypeError("RGB values between 1 and 16 flicker.")
	return cvalue

def check_COLOR(value):
	from ledlib.colordefs import colortable
	if value == "":
		return value
	if value in colortable:
		return value
	else:
		raise argparse.ArgumentTypeError("Unknown color " + value)

def check_RESO(value):
	try:
		ivalue = int(value)
	except:
		raise argparse.ArgumentTypeError("Resonator number must be between 0 and 7")

	if (ivalue < 0) or (ivalue > 7):
		raise argparse.ArgumentTypeError("Resonator number must be between 0 and 7")
	return value

def legal_intensity(value):
	if value < 8:
		return 0
	if value < 16:
		return 16
	if value < 255:
		return int(value)
	else:
		return 255


def dimmer (rgb_triplet, scale=1.00, maxbright=globalconfig.max_brightness):
	# usage:  new_rbg = dimmer(old_rgb)				# flatten down over-brightness
	#					new_rgb = dimmer(old_rgb, 0.6)	# 60%
	# RGB_min = ledmath.RGB_min
	# RGB_max = ledmath.RGB_max
	red = rgb_triplet[0]
	green = rgb_triplet[1]
	blue = rgb_triplet[2]

	if (scale < 1.00):
		red = red * scale
		green = green * scale
		blue = blue * scale

	average_brightness = (red + green + blue) / 3
	percent_brightness = average_brightness / RGB_max
	if (percent_brightness) > maxbright:
		red = red * maxbright * percent_brightness
		green = green * maxbright * percent_brightness
		blue = blue * maxbright * percent_brightness

	red = legal_intensity(red)
	green = legal_intensity(green)
	blue = legal_intensity(blue)

	return (red, green, blue)

def mix (rgb1, scale1, rgb2, scale2=0, maxbright=globalconfig.max_brightness):
	# mix two colors in the given proportions.
	# more Pythonic to have the inputs be structured.  Feel free to fix.
	# scale1 and scale2 will not necessarily sum to 1
	if scale2==0:
		scale2 = 1.0-scale1
	red		= rgb1[0]*scale1 + rgb2[0]*scale2
	green	= rgb1[1]*scale1 + rgb2[1]*scale2
	blue	= rgb1[2]*scale1 + rgb2[2]*scale2
	return dimmer((int(red), int(green), int(blue)))

	pass

