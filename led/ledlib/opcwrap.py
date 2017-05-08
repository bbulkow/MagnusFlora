# opc interface, to hide the ugly.

import opc
import time
from ledlib.hardcode import fcserverconfig
from ledlib import globalconfig
from ledlib import globaldata
from ledlib.helpers import debugprint

def check_fcs(server,port):
	# make sure that the Fadecandy server is up
	# sudo fcserver ~/etc/fcserver.json
	pass

def start_opc():
	server = fcserverconfig.server
	port = fcserverconfig.port
	check_fcs(server,port)

	# Create a client object
	client_home = "".join([server,":",port])
	client = opc.Client(client_home)

	# Test if it can connect (optional)
	if client.can_connect():
		print('connected to %s' % client_home)
	else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
		print('WARNING: could not connect to %s' % client_home)

	return client

def ledwrite(client, pixels):				# should be a method in a class
	# ugly workaround suggested on stack overflow
	if not globalconfig.noop:
		client.put_pixels(pixels)
		client.put_pixels(pixels)


def ledwriteloop():
	# designed to run in a very simple thread

	while True:
		# ugly workaround suggested on stack overflow
		if not globalconfig.noop:
			globaldata.ledcontrol.put_pixels(globaldata.all_the_pixels)
			globaldata.ledcontrol.put_pixels(globaldata.all_the_pixels)
		time.sleep(globalconfig.framedelay)
		debugprint ("Tick... ")



