
numLEDs = 512
StripSize = 30
# first pixel on each Fadecandy port
Bases = [ 0, 64, 128, 192, 256, 320, 384, 448 ]

def pixel_list (Fadecandy, strand, chunk, chunksize=30, direction=0):
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
	print ("head = "+str(chunkhead))
	print ("tail = "+str(chunktail))

	pixels = [0] * chunksize
	for i in range (chunksize):
		if direction == 0:
			pixels[i] = chunkhead + i
		if direction == 1:
			pixels[i] = chunktail - i
	
	


def wrap():
  pass

