# basic Flask shell for the TechThulu Simultor

# WARNING. This code DOES NOT WORK.
# There is no stable and reasonable way to read from a file in the background
# in Flask. There are a number of hints and tricks, but Flask doesn't support it.
# 

"""
Made available under the MIT license

Copyright 2017 Brian Bulkowski brian@bulkowski.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from flask import Flask
from flask import request
import threading
import atexit
import time

app = Flask(__name__)

# choose the config object here:
# Production, Development, Testing
app.config.from_object('config.DevelopmentConfig')

# this function gets the next \n configured line from the file



# Relay class 
class Relay:
	def __init__(self):
		# 1 is "NO and NC", 0 is "Flipped"
		self.state = 0

		# 0, 1, 2, 3 are possible
		# 1 = relay is NC /NO when portal is controlled, reversed when neutral
		# 2 = relay is reversed when portal is controlled, NO/NC when neutral
		# 3 = relay is NC /NO when portal is controlled, reversed for 3 seconds when faction changes, then reverts to NO/NC
		# 4 = relay closed when portal is controlled, reversed for 1.5 seconds
		self.mode = 0


# todo: since a mod has an owner, should make it a class as well, for parallelism sake


# Resonator class... because portals have more than one resonator

class Resonator:
	def __init__(self, position):
		self.level = 0
		self.health = 0
		self.distance = 0
		self.position = position

	def check(self):
		if type(self.level) is not int:
			return False
		if self.level < 0 or self.level > 8:
			return False
		if self.health is not int:
			return False
		if self.health < 0 or self.health > 100:
			return False
		if type(self.position) is not str:
			return False
		if self.position not in valid_positions:
			return False
		if self.distance is not int:
			return False
		if self.distance < 0 or self.distance > 100:
			return False
		return True

	def setLevel(self, level):
		# wire up debugging....
		if level > 8:
			return False
		if level < 0:
			return False
		self.level = level
		if level == 0:
			self.health = 0
			self.distance = 0
		return True

	def setHealth(self, health):
		if health > 100:
			return False
		if health < 0:
			return False
		self.health = health
		if health == 0:
			self.level = 0
			self.distance = 0
		return True

	def __str__(self):
		return '{"level": {0}, "health": {1}, "distance": {2}, "position": {3}}'.format(self.level, self.health, self.distance, self.position)

	# without the position, sometimes that is implied 
	def toBetterStr(self):
		return '{"level": {0}, "health": {1}, "distance": {2}}'.format(self.level, self.health, self.distance)

# WARNING! This class has multithreaded access.
# Before you access the data structure, grab the lock and release afterward
# do not do anything blocking under the lock
class Portal:

	valid_positions = [ "E", "NE", "N", "NW", "W", "SW", "S", "SE" ]
	valid_mods = ["FA","HS-C","HS-R","HS-VR","LA-R","LA-VR","SBUL","MH-C","MH-R","MH-VR","PM","PS-C","PS-R","PS-VR","AXA","T"]

	def __init__(self, id_):
		self.faction = 0
		self.health = 0
		self.level = 0
		self.id_ = id_
		self.title = "default portal"
		self.owner = ""
		self.owner_id = 0
		self.resonators = {	"N": Resonator("N"),
							"NE": Resonator("NE"),
							"E": Resonator("E"),
							"SE": Resonator("SE"),
							"S": Resonator("S"), 
							"SW": Resonator("SW"), 
							"W": Resonator("W"),
							"NW": Resonator("NW") 
		}
		self.links = []
		self.mods = [ None, None, None, None ]
		self.lock = threading.Lock()  
		self.create_time = time.time()
		print("Created a new portal object")  


	# This is the "current form" that is mussing a lot of information
	def __str__(self):
		resos = []
		resos.append('resonators: [')
		for r in self.resonators:
			# skip if empty, saving space & time
			if r.level == 0:
				continue
			resos.append(str(r))
		resos.append(']')
		reso_string = ''.join(resos)
		return '"controllingFaction": {0}, "health": {1}, "level": {2}, "title": "{3}", "resonators": {4}'.format( 
			self.faction, self.health, self.level, self.title, reso_string )

	def toBetterStr(self):
		# shortcut
		if level == 0:
			if level == 0:
				return '"faction": 0, "health":0, "level":0, "title":{0}, "resonators": []'.format(self.title)
		#longcut
		resos = []
		resos.append('resonators: [')
		for r in self.resonators:
			# skip if empty, saving space & time
			if r.level == 0:
				continue
			resos.append(r.toBetterStr())
		resos.append(']')
		reso_string = ''.join(resos)
		return '"faction": {0}, "health": {1}, "level": {2}, "title": "{3}", "resonators": {4}'.format( 
			self.faction, self.health, self.level, self.title, reso_string )

	# this method makes sure the status is valid and reasonable ( no values greater than game state )
	def check(self):
		if type(self.faction) is not int:
			print("Portal faction type initvalid")
			return False
		if self.faction < 0 or self.faction > 2:
			print("Illegal Portal faction value ",self.faction)
			return False
		if type(self.health) is not int:
			print("Portal health type invalid")
			return False
		if self.health < 0 or self.health > 100:
			print("Illegal Portal health value ",self.health)
			return False
		if type(self.level) is not int:
			print("Portal level type invalid")
			return False
		if self.health < 0 or self.health > 8:
			print("Illegal Portal level value ",self.level)
			return False
		if type(self.title) is not str:
			print("Portal title type invalid")
			return False
		if len(self.title) > 300:
			print("Portal title seems too long")
			return False
		if type(self.resonators) is not dict:
			print("Portal resonator type wrong")
			return False
		if len(self.resonators) != 8:
			print("Portal has incorrect number of resonators ",len(self.resontaors))
			return False
		for r in valid_positions:
			if checkResontaor(self.resonator[r]) == False:
				print(" resonator ",r," is not valid ")
				return False
		if type(self.mods) is not list:
			print("Mods wrong type")
			return False
		if len(self.mods) > 4:
			print("too many mods")
			return False
		for m in mods:
			if type(m) is not str:
				print (" type of one of the mods is wrong ")
				return False
			if m not in valid_mods:
				print ("invalid mod ",m)
				return False
		return True

# The Portal
g_portal = Portal(1)

# you might ask why not use the API manager. The API manager creates,
# AFAIK, a specific URL pattern ( API ), which is not part of our spec.
# Thus it is better to just do this.

@app.route('/')
def hello_world():
	return 'Hello World! I am the TechThulu Simulatron!'

@app.route('/status/faction')
def statusFaction():
	global g_portal
	return str(g_portal.faction)

@app.route('/status/health')
def statusHealth():
	global g_portal
	with g_portal.lock:
		return str(g_portal.health)
	

@app.route('/status/json')
def statusJson():
	global g_portal
	with g_portal.lock:
		return g_portal.getStatusString()

# The Relay
g_relay = Relay()

# commands not currently supported - but at least it'll act like something
@app.route('/command/relay/get_mode')
def commandRelayGetMode():
	global g_relay
	return str(g_relay.mode)

@app.route('/command/relay/get_mode')
def commandRelayGetState():
	global g_relay
	return str(g_relay.state)

# todo: the 
@app.route('/command/relay/set_manual', methods=['POST'])
def commandRelaySetManual():
	global g_relay
	return ""

backgroundTimer = None

# app control things: because I am using threading for a background task ( instead of celery or anything else )
def interrupt():
	global backgroundTimer
	if backgroundTimer:
		backgroundTimer.cancel()
		backgroundTimer = None

def backgroundFn():
	global backgroundTimer
	backgroundTimer = None

	global g_portal
	print( "I am the background thread!!! portal object create time: ",g_portal.create_time)

	backgroundTimer = threading.Timer(5.0,backgroundFn,())
	backgroundTimer.start()

def startBackground():
	global backgroundTimer
	backgroundTimer = threading.Timer(0.0,backgroundFn,())
	backgroundTimer.start()
	atexit.register(interrupt)


if __name__ == '__main__':
#	from werkzeug.serving import is_running_from_reloader
#	if is_running_from_reloader() == False:
#		startBackground()
	startBackground()
	app.run()
