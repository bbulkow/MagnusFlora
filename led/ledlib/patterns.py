import random
import time

def randomcolor(maxbright=.5):
	# not really random: everything over maxbright collapses to same intensity
	from ledlib import ledmath

	RGB_min = ledmath.RGB_min
	RGB_max = ledmath.RGB_max

	# TODO: add a parameter to control possible brightness
	red = random.randint(RGB_min,RGB_max)
	green = random.randint(RGB_min,RGB_max)
	blue = random.randint(RGB_min,RGB_max)
	average_brightness = (red + green + blue) / 3
	percent_brightness = average_brightness / RGB_max
	if (percent_brightness) > maxbright:
		red = int ( (red * maxbright) * percent_brightness)
		green = int ( (green * maxbright) * percent_brightness)
		blue = int ( (blue * maxbright) * percent_brightness)
	print (red, green, blue)
	return (red, green, blue)


def wake_up (first, size, rgb_color_triplet):
	from ledlib.helpers import debugprint
	from ledlib import globalconfig
	from ledlib import globaldata

	debugprint ("Waking up "+ str(size) + " pixels")
	print (rgb_color_triplet)

	shuffled_index = [ 0 ] * size
	for i in range (size):
		shuffled_index[i] = i
	random.shuffle (shuffled_index)

	for i in range (size):
		# even without a sleep this took visible time to run.  not a good sign.
		# but setting to a single color was very fast
		globaldata.all_the_pixels[shuffled_index[i]] = randomcolor()
		time.sleep (globalconfig.twinkle/2)

	time.sleep (10 * globalconfig.framedelay)

	# shuffle again
	random.shuffle (shuffled_index)
	for i in range (size):
		globaldata.all_the_pixels[shuffled_index[i]] = rgb_color_triplet
		time.sleep (globalconfig.twinkle)


