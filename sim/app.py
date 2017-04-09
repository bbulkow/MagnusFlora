# basic flask shell for the TechThulu Simultor
# (c) Brian Bulkowski, 2017
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.

from flask import Flask
from flask import request

app = Flask(__name__)

# choose the config object here:
# Production, Development, Testing
app.config.from_object('config.DevelopmentConfig')

# 

# TODO: write a generator function that will get the next line in the next file

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


# portal class... in case you ever want more than one portal

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


# TODO: add modifiers, 
class Portal:

	valid_positions = [ "E", "NE", "N", "NW", "W", "SW", "S", "SE" ]
	valid_mods = ["FA","HS-C","HS-R","HS-VR","LA-R","LA-VR","SBUL","MH-C","MH-R","MH-VR","PM","PS-C","PS-R","PS-VR","AXA","T"]

	def __init__(self):
		self.faction = 0
		self.health = 0
		self.level = 0
		self.title = "default portal"
		self.resonators = {	"N": Resonator("N"),
							"NE": Resonator("NE"),
							"E": Resonator("E"),
							"SE": Resonator("SE"),
							"S": Resonator("S"), 
							"SW": Resonator("SW"), 
							"W": Resonator("W"),
							"NW": Resonator("NW") 
		}
		self.mods = [ None, None, None, None ]

	# TODO
	def getStatusString(self):
		return ""

	def checkResonator(r):
		if type(r["level"]) is not int:
			return False
		if r["level"] < 0 or r["level"] > 8:
			return False
		if type(r["health"]) is not int:
			return False
		if r["health"] < 0 or r["health"] > 100:
			return False
		if type(r["position"]) is not str:
			return False
		if r["position"] not in valid_positions:
			return False
		if type(r["distance"]) is not int:
			return False
		if r["distance"] < 0 or r["distance"] > 100:
			return False
		return True


	# this method makes sure the status is valid and reasonable ( no values greater than game state )
	def check(self):
		if type(self.faction) is not int:
			print("Portal faction type invalid")
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
				print(" resonator ",idx," is not valid ")
				return False
		return True

# The Portal
g_portal = Portal()

# you might ask why not use the API manager. The API manager creates,
# AFAIK, a specific URL pattern ( API ), which is not part of our spec.
# Thus it is better to just do this.

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/status/faction')
def statusFaction():
	global g_portal
	return str(g_portal.faction)

@app.route('/status/health')
def statusHealth():
	global g_portal
	return str(g_portal.health)

@app.route('/status/json')
def statusJson():
	global g_portal
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


if __name__ == '__main__':
	app.run()
