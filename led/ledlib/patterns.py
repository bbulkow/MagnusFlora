import random
import time
from ledlib.helpers import debugprint, verboseprint
from ledlib import ledmath

from ledlib import globalconfig
from ledlib import globaldata
from ledlib import masking

static_patterns = ["SOLID", "BLEND", "DIM", "TEST"]
moving_patterns	=	["TWINKLE", "FLOOD", "FLASH",
									"SHAKE", "CHASE", "MORSE", "MOVINGTEST"]

portal_patterns = ["NEUTRALIZE", "FRACK", "ADA", "JARVIS"]

defined_patterns = static_patterns + moving_patterns + portal_patterns

def check_PATTERN(pname):
	pstring = str(pname)
	if (pstring in defined_patterns):
		return pstring
	else:
		raise argparse.ArgumentTypeError("Unknown pattern name")

def randomcolor(maxbright=.5):
	# not really random: everything over maxbright collapses to same intensity
	from ledlib import ledmath
	# Note well: maxbright is permitted to be larger than global

	RGB_min = ledmath.RGB_min
	RGB_max = ledmath.RGB_max

	# TODO: add a parameter to control possible brightness
	red = random.randint(RGB_min,RGB_max)
	green = random.randint(RGB_min,RGB_max)
	blue = random.randint(RGB_min,RGB_max)

	debugprint (("random: ", red, green, blue))			# print tuple, not 3 singles
	rgb = ledmath.dimmer((red,  green, blue),1.0,maxbright)
	debugprint (("dimmed: ", rgb))
	return rgb

# this is an actual pattern.
# it uses globalconfig.twinkle to figure out the speed
# it covers "all the pixels"

def wake_up (first, size, rgb_color_triplet):
	debugprint ("Waking up "+ str(size) + " pixels")
	debugprint (rgb_color_triplet)

	if globalconfig.fastwake:
		for i in range(size):
			globaldata.all_the_pixels[first+i] = rgb_color_triplet
	else:
		shuffled_index = [ 0 ] * size
		for i in range (size):
			shuffled_index[i] = i
		random.shuffle (shuffled_index)

		for i in range (size):
			# even without a sleep this took visible time to run.  not a good sign.
			# but setting to a single color was very fast
			globaldata.all_the_pixels[first+shuffled_index[i]] = randomcolor()
			time.sleep (globalconfig.twinkle/4)

		time.sleep (10 * globalconfig.framedelay)

		# shuffle again
		random.shuffle (shuffled_index)
		for i in range (size):
			globaldata.all_the_pixels[first+shuffled_index[i]] = rgb_color_triplet
			time.sleep (globalconfig.twinkle)

# 

def fade (list_of_pixel_numbers, rgb_color_triplet, fade_ratio=0.5, speed=0):
	# pixel 0 is at 100%; pixel last is at fade_ratio; if sleep defined
	# sleep after setting every pixel

	size = len(list_of_pixel_numbers)

	globaldata.all_the_pixels[list_of_pixel_numbers[0]]=rgb_color_triplet
	for i in range(1,size):
		fade = 1.0 - ((i/size)*fade_ratio)
		debugprint ((i,fade))
		globaldata.all_the_pixels[list_of_pixel_numbers[i]]= \
						dimmer(rgb_color_triplet,fade)
		if speed > 0:
			time.sleep(speed)

# This goes from rgb1 to rgb2 along each list of pixel numbers

def parallel_blend (list_of_lists_of_pixel_numbers, \
										rgb1, rgb2, speed=0, steps=100):
	# pixel 0 is at 100%; pixel last is at fade_ratio;
	# smooth gradient along multiple strands of LEDs of different lengths.

	strand_count = len(list_of_lists_of_pixel_numbers)
	strand_sizes = [0] * strand_count
	strand_pointers = [0] * strand_count

	debugprint (("blend between", rgb1, rgb2))

	for strand in range(strand_count):
		strand_sizes[strand] = len(list_of_lists_of_pixel_numbers[strand])
		debugprint (("Strand ", strand, "size ", strand_sizes[strand], "begin", list_of_lists_of_pixel_numbers[strand][0]))
		globaldata.all_the_pixels \
					[list_of_lists_of_pixel_numbers[strand][0]]=rgb1


	for thisstep in range(steps):
		# ignore the fencepost errors.  not going for exactness here.
		# hue will vary due to rounding.  possibly a feature.
		progress = thisstep/steps
		newcolor = ledmath.mix(rgb1, 1.0-progress, rgb2)
		debugprint (("blend", thisstep, newcolor))
		for strand in range(strand_count):
			while progress > (strand_pointers[strand] / strand_sizes[strand]):
				globaldata.all_the_pixels \
					[list_of_lists_of_pixel_numbers[strand][strand_pointers[strand]]] = \
							newcolor
				strand_pointers[strand] += 1
		if speed > 0:
			time.sleep(speed/steps)

	# nail in the last pixel in each strand
	for strand in range(strand_count):
		last_pixel = list_of_lists_of_pixel_numbers[strand][strand_sizes[strand]-1]
		debugprint (("Last pixel, setting end of strand ", str(strand), "pixel number " , str(last_pixel), "rgb2", rgb2))
		# globaldata.all_the_pixels \
	#			[list_of_lists_of_pixel_numbers[strand][strand_sizes[strand]-1]]= \
				#rgb2
		globaldata.all_the_pixels[last_pixel] = rgb2


def chase (list_of_lists_of_pixel_numbers, maskstring, repeat):
	# note that this should support a chase on only some components of a reso
	# repeat = -1 : infinite repeat
	strand_count = len(list_of_lists_of_pixel_numbers)
	strand_sizes = [0] * strand_count
	strand_pointers = [0] * strand_count
	base_pixels	=	[0,0,0] * strand_sizes[0] * strand_count
	# TODO: should be configurable params
	steps = 200
	speed = 3			# how long to do one pass?
	chasemask = masking.Mask(maskstring)
	print ("entering chase loop with %s", chasemask.name)

	def __single_chase(base_pixels, list_of_lists_of_pixel_numbers, chasemask, steps, speed):
		print ("entering single chase with %s", chasemask.name)
		strand_pointers = [0] * strand_count
		for thisstep in range(steps):
			progress = thisstep/steps
			for strand in range(strand_count):
				while progress > (strand_pointers[strand] / (strand_sizes[strand]+chasemask.size)):
					for i in range(chasemask.size):
							# set previous N pixels (if in bounds) to base
							backpix = strand_pointers[strand] - chasemask.size - i
							if backpix >=0:
								#globaldata.all_the_pixels \
								#			[list_of_lists_of_pixel_numbers[strand][backpix]] = \
								#			base_pixels[strand][backpix]
								print ("line 164")
								globaldata.setpixel(list_of_lists_of_pixel_numbers[strand][backpix], base_pixels[strand][backpix])
							# set current N pixels (if in bounds) to masked base
							frontpix = strand_pointers[strand] - i
							leadpix = min(frontpix + chasemask.size, strand_sizes[strand])
							if frontpix >= 0 and frontpix < strand_sizes[strand] and leadpix > frontpix:
											# temp hardcode for algo testing
								#globaldata.all_the_pixels \
											#[list_of_lists_of_pixel_numbers[strand][frontpix]] = \
											#[200,50,50]
								print ("frontpix = ", frontpix, "leadpix= ", leadpix)
								masked_pixels = chasemask.apply(globaldata.all_the_pixels[frontpix:leadpix])
								print ("line 175", "frontpix = ", frontpix, "i= ", i)
								try:
									globaldata.setpixel(list_of_lists_of_pixel_numbers[strand][frontpix], masked_pixels[i])
								except:
									# fencepost somewhere.
									pass
					strand_pointers[strand] += 1
			if speed > 0:
				time.sleep(speed/steps)
# 		# clear out the final chase area
# 		for i in range(chasemask.size):
# 			backpix = strand_sizes[strand] - (chasemask.size - i)
# 			if backpix >= 0:
# 				globaldata.setpixel( \
# 							[list_of_lists_of_pixel_numbers[strand][backpix]], \
# 							base_pixels[strand][backpix])
# 			if speed > 0:
# 				time.sleep(speed/steps)
		# return to base state
		print ("returning to base state")
		for strand in range(strand_count):
			for i in range(strand_sizes[strand]):
				globaldata.setpixel(list_of_lists_of_pixel_numbers[strand][i], base_pixels[strand][i])


	base_pixels = [0,0,0] * strand_count * 1
	for strand in range(strand_count):
		strand_sizes[strand] = len(list_of_lists_of_pixel_numbers[strand])
		# TODO: dimension and fill in one step
		# quite doable see http://stackoverflow.com/questions/10623302/how-assignment-works-with-python-list-slice
		base_pixels[strand] = [0,0,0] * strand_sizes[strand]
		for pix in range(strand_sizes[strand]):
			base_pixels[strand][pix] = \
						globaldata.all_the_pixels[list_of_lists_of_pixel_numbers[strand][pix]]

	if repeat >= 1:
		for loop in range(repeat):
			__single_chase(base_pixels, list_of_lists_of_pixel_numbers, chasemask, steps, speed)
	else:
		while True:
			__single_chase(base_pixels, list_of_lists_of_pixel_numbers, chasemask, steps, speed)


# this fades along each list of pixesl

def parallel_fade (list_of_lists_of_pixel_numbers, \
										rgb_color_triplet, fade_ratio=0.5, speed=0, steps=100):
	# pixel 0 is at 100%; pixel last is at fade_ratio;
	# smooth gradient along multiple strands of LEDs of different lengths.

	strand_count = len(list_of_lists_of_pixel_numbers)
	strand_sizes = [0] * strand_count
	strand_pointers = [0] * strand_count
	for strand in range(strand_count):
		strand_sizes[strand] = len(list_of_lists_of_pixel_numbers[strand])
		debugprint (("Strand ", strand, "size ", strand_sizes[strand]))
		globaldata.all_the_pixels \
					[list_of_lists_of_pixel_numbers[strand][0]]=rgb_color_triplet


	for thisstep in range(steps):
		# ignore the fencepost errors.  not going for exactness here.
		# hue will vary due to rounding.  possibly a feature.
		brightness = 1.0 - fade_ratio*thisstep/steps
		newcolor = ledmath.dimmer(rgb_color_triplet, brightness)
		debugprint (("fade", thisstep, brightness, newcolor))
		progress = thisstep/steps
		for strand in range(strand_count):
			while progress > (strand_pointers[strand] / strand_sizes[strand]):
				globaldata.all_the_pixels \
					[list_of_lists_of_pixel_numbers[strand][strand_pointers[strand]]] = \
							newcolor
				strand_pointers[strand] += 1
		if speed > 0:
			time.sleep(speed/steps)

	# nail in the last pixel in each strand
	newcolor = ledmath.dimmer(rgb_color_triplet, fade_ratio)
	for strand in range(strand_count):
		globaldata.all_the_pixels \
				[list_of_lists_of_pixel_numbers[strand][strand_sizes[strand-1]]]= \
				newcolor


# set a list-of-lists to a single color
def set_color(pixel_numbers_lol, rgb):
	for strand in pixel_numbers_lol:
		for p in strand:
			debugprint(("set_color: setting to "))
			globaldata.all_the_pixels[p]= rgb



# set a list-of-lists to a previously captured color
#     SOURCE is the rgb_values_lol where values were stashed
#     DEST is the global memory array
def set_values(pixel_numbers_lol, rgb_values_lol):

	strand_count = len(pixel_numbers_lol)

	for strand_n in range(0,strand_count):
		strand_len = len( pixel_numbers_lol[ strand_n ] )
		for p_n in range(0,strand_len):
			globaldata.all_the_pixels[ pixel_numbers_lol[strand_n][p_n] ] = rgb_values_lol [strand_n] [p_n]



# flashes a particular RGB
# ends up with the old pattern after the flashes
# number of flashes you want to do
# speed is total amount of time in float seconds

def flash ( pixel_numbers_lol, rgb, n_flashes, secs ):

	strand_count = len(pixel_numbers_lol)
	strand_sizes = [0] * strand_count
	for strand in range(strand_count):
		strand_sizes[strand] = len(pixel_numbers_lol[strand])

	old_pixel_values = [0] * strand_count

	# take a duplicate of all the old valuescopy the curent values of all the lists of lists
	# you will have strands with RGB in them, not with pixel values
	for strand_n in range(0,strand_count):
		strand = pixel_numbers_lol[strand_n]
		old_pixel_values[strand_n] = [0] * len(strand)
		for idx in range(0,len(strand)):
			old_pixel_values[strand_n][idx] = globaldata.all_the_pixels[strand[idx]]

	# todo: would really like the flashes to get faster instead of being all-the-same
	flash_time = secs / n_flashes
	flash_time = flash_time / 2.0    # on and off

	# for the number of flashes
	for i in range(0,n_flashes):

		# set all the values to known number
		set_color( pixel_numbers_lol, rgb)

		time.sleep(flash_time)

		# set all the values back to what I grabbed before
		set_values( pixel_numbers_lol, old_pixel_values)

		time.sleep(flash_time)









