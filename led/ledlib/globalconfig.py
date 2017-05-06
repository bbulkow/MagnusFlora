#
# global variables seen within multiple modules
# Usage:
#   import globalconfig
#   globalconfig.debugflag = True

# defaults for script command-line options
debugflag = False
verboseflag = False
batchmode = False
noop = False

# UI defaults
prompt = "Magnus Flora> "		# TODO: investigate using sys.ps2

# store variables that should only be populated once
fqdn = ""
hostname = ""		# short hostname, first part of FQDN
effectiveuser = ""	# i.e. root
humanuser = ""		# i.e. the user who becme root

fastwake				= False

# shared memory across threads

heartbeat				= 0			# loop for a timer.
synchseconds		=	3			# everything syncs after X seconds
heartrate				= 0.05	# 20 ticks per second
heartmax				= synchseconds / heartrate
												# ticks per synchronization cycle

polling_interval = 0.1	# talk to Jarvis 10 times a second

# write frames to the pixels every hundredth of a second
framedelay				=	0.01

# delay between writes when twinkling in a solid color
twinkle						=	framedelay / 10

max_brightness		=	0.8		# default for dimmer function
