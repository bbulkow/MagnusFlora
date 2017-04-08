This program will create a Flask web service which emulates the Niantic TechThulu module.

The spec for the project's endpoints and rest addresses are like this:

# TechTHulu specs as of April 8, 2017

/module/status/json - Returns a JSON string of detected information for portal (example below)

/module/status/faction - Returns 0 (Neutral), 1 (Enlightened), 2 (Resistance)

/module/status/health - Returns 0-100 (aggregated % of charges on deployed resonators)

/module/command/relay/get_mode - returns the mode of the relay {0,1,2,3}

/module/command/relay/get_state - 1 = (N.O and N.C) || 0 = (state is flipped)

/module/command/relay/set_manual - puts the relay into manual control mode

/module/command/relay/set_auto1 - puts the relay into automatic control mode 1

/module/command/relay/set_auto2 - puts the relay into automatic control mode 2

/module/command/relay/set_auto3 - puts the relay into automatic control mode 3

- 1 = relay is NC /NO when portal is controlled, reversed when neutral
- 2 = relay is reversed when portal is controlled, NO/NC when neutral
- 3 = relay is NC /NO when portal is controlled, reversed for 3 seconds when faction changes, then reverts to NO/NC
- 4 = relay closed when portal is controlled, reversed for 1.5 seconds

when total resonator count decreases.

/module/command/relay/high - Sets relay into default NO/NC state (paradoxically high cuz, reasons)

/module/command/relay/low - Energizes the relay and flips NO and NC.

/module/command/relay/toggle - flips relay state regardless (and forces it into manual mode)

/module/command/diagnostics - Returns title of portal, runs short diagnostics, then fully resets/restarts module

# Endpoint Examples

Send: "tecthulhu_module03.local/module/status/title"
Receive: "Camp Navarro"

Send: "tecthulhu_module07.local/status/faction”
Receive: 0

Send: "tecthulhu_module11.local/module/command/relay/toggle
Receive: "OMG! Stop with the air horn already, it's 2 AM!!"

Send: "tecthulhu_module09.local/module/status/json"
Receive: "status": {
	"controllingFaction": "2",
	"level": 6,
	"health": 96,
	"title": "Camp Navarro"
	"resonators": [
		{"level": 6,"health": 94,"owner": "NumberSix","position": "E"},
		{"level": 6,"health": 96,"owner": "NumberSix","position": "NE"},
		{"level": 7,"health": 97,"owner": "NumberSix","position": "N"},
		{"level": 8,"health": 97,"owner": "NumberSix","position": "NW"},
		{"level": 6,"health": 97,"owner": "NumberSix","position": "W"},
		{"level": 7,"health": 96,"owner": "NumberSix","position": "SW"},
		{"level": 8,"health": 94,"owner": "NumberSix","position": "S"},
		{"level": 7,"health": 94,"owner": "NumberSix","position": "SE"}
		]
	}

Proposed would be:
	"resonators": {
		"E": {"level": 6,"health": 94,"owner": "NumberSix"},
		"NE": {"level": 6,"health": 94,"owner": "NumberSix"},
		"N": {"level": 6,"health": 96,"owner": "NumberSix"},
		"NW": {"level": 7,"health": 97,"owner": "NumberSix"},
		"W": {"level": 6,"health": 97,"owner": "NumberSix"},
		"SW": {"level": 7,"health": 96,"owner": "NumberSix"},
		"S": {"level": 8,"health": 94,"owner": "NumberSix"},
		"SE": {"level": 7,"health": 94,"owner": "NumberSix"}
	}
