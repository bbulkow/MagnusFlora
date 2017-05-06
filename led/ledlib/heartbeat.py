heartbeat = 0

def ticktock(startfrom=0):
	from ledlib.globalconfig import heartbeat, heartmax, heartrate
	global heartbeat
	from time import sleep
	from ledlib.helpers import debugprint
	heartbeat = startfrom
	while True:
		if heartbeat >= heartmax:		# should never be >
			heartbeat = 0
			debugprint ("Tick loudly... ")
		else:
			heartbeat += 1
		sleep (heartrate)

# def start_heartbeat():
# 	# TODO: use import threading from python3
# 	from _thread import start_new_thread
# 	start_new_thread(ticktock, (0,))

def wait_for_heartbeat(pulse):
	from time import sleep
	from ledlib.helpers import debugprint
	from ledlib.globalconfig import heartbeat, heartmax, heartrate
	global heartbeat
	if pulse > heartmax:
		debugprint (("Setting pulse to ", pulse, heartmax))
		pulse = heartmax
	while True:
		debugprint (("Wait for absolute pulse:", heartbeat, pulse))
		if heartbeat == pulse:
			break
		sleep (heartrate/4)

def wait_for_heartbeat(percent):
	from time import sleep
	from ledlib.helpers import debugprint
	from ledlib.globalconfig import heartbeat, heartmax, heartrate
	if percent > 100:
		debugprint (("Bad percent ", percent))
		percent = 100
	while True:
		debugprint (("Wait for absolute pulse:", heartbeat, pulse))
		if heartbeat == pulse:
			break
		sleep (heartrate/4)


