#!/usr/bin/env python3

import time
from ledlib import opc
from ledlib import globalconfig, heartbeat
from ledlib.helpers import *

def read_config():
	debugprint ("in read_config")

def setup_fadecandy():
	debugprint ("in setup_fadecandy")

def setup_portal_components():
	debugprint ("in setup_portal_components")

def talk_to_Jarvis():
	debugprint ("talk to the hand")
	heartbeat.wait_for_heartbeat(15)
	print ("heartbeat = 15")

def talk_to_portal():
	debugprint ("talk to the wall.")

heartbeat.start_heartbeat()	# single thread that loops a global variable.
read_config()
setup_fadecandy()
setup_portal_components()	# start threads for each 

while True:
    talk_to_Jarvis()
    talk_to_portal()
    time.sleep (globalconfig.polling_interval)



