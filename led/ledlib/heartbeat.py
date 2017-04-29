heartbeat = 0

def ticktock(startfrom):
	from ledlib.globalconfig import heartbeat, heartmax, heartrate
	global heartbeat
	from time import sleep
	from ledlib.helpers import debugprint
	heartbeat = startfrom
	while True:
		if heartbeat >= heartmax: 		# should never be >
			heartbeat = 0
			debugprint ("Tick")
			print ("Tick loudly... ")
		else:
			heartbeat += 1
		sleep (heartrate)
		
	

def start_heartbeat():
	# TODO: use import threading from python3
	from _thread import start_new_thread
	start_new_thread(ticktock, (0,))

def wait_for_heartbeat(pulse):
	from time import sleep
	from ledlib.helpers import debugprint
	from ledlib.globalconfig import heartbeat, heartmax, heartrate
	global heartbeat
	while True:
		print (heartbeat, pulse)
		if heartbeat == pulse:
			break
		sleep (heartrate/4)

