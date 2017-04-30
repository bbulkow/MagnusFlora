# ledmath.py

RGB_min = 16		# below this we get flicker.  Disallow or use Fadecandy dither

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



