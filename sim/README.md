This program will create a web service which emulates the Niantic TechThulu module.

# Running the program

This requires python 3 ( probably Python 3.5 ) and the aiohttp module. Install using 'pip install aiohttp' as necessary.

Then: `python portal_sim.py`

## Options

`--port` will specify the HTTP port ( default 5050 )

`--legacy` will use the format created by Niantic, which does not include Mods, Resonator position or owners

`--file` will specify a Json simulation filename. ( default: techthulu.json )

# Known Limitations

The Relay is not wired up generally, and not wired to an actual relay. This is "todo"

Owners on Mods is not supported

# How it works

In order to simulate the state and timing of a rest endpoint, a simulation file is used.

These simulation files are written in streaming JSON. Each line is a JSON object. Besides having variables that are set, there is an optional "delay" element in the JSON object. This allows the file to encode timing.

In order to efficiently read a file in the background of serving a web endpoint, a number of frameworks were considered.
The simplest seemed to be the newer `aiohttp` module, which has the benefit of fully async processing. This allows


# Writing simulation files

A line in a file is allowed to have a `#` as the first character, which means the line will be skipped.

A "delay" item will specify, in fractional seconds, the amount of time before the next line is read and processed.

Two items in the output ( Level and Health ) are generated from the resonator state.

Any item can be skipped in any object, in which case the prior values will be used. This can be used to easily decrease or increase resonators without repeating the entire object.

In any JSON line, if an error is found ( like invalid JSON, or an invalid modifier string or resonator position ), an error will be printed and that line will be skipped - which means the delay will not be processed, either.

The following JSON fields are allowed:

- `title` The name of the portal. Always UTF-8.
- `faction` 0 - unowned , 1 - Enlightened , 2 - Resistance
- `owner` UTF-8 string representing the owner
- `resonators` A dictionary of resontaor states, indexed by the positional location ( see below  )
- `mods` An array of portal modifiers. This replaces other modifiers, all-or-nothing

## Modifiers

- `FA`
- `HS-C`
- `HS-R`
- `HS-VR`
- `LA-R`
- `LA-VR`
- `SBUL`
- `MH-C`
- `MH-R`
- `MH-VR`
- `PM`
- `PS-C`
- `PS-R`
- `PS-VR`
- `AXA`
- `T`

## Resonators

A resonator item will have a position, which is a direction aligned with true north, as per game place.

It one of `N` , `NE` , `E`, `SE`, `S`, `SW`, `W`, `NW`

The dictionary associated with a resontor includes:

- `health` - the current health value, from 0 if unowned, to 100 if full
- `owner` - the string representing who has placed the resonator, omitted if unowned
- `level` - the level of the resonator, an integer, or 0 if unowned
- `distance` - a scale of 0 to 100, representing how far a resonator is from the portal

## Example

```
   { "delay": 0.0, "title": "myportal", "faction": "1", "owner": "bbulkow", "mods": [ "PS-C", "HS-C", "HS-R" ]  }
   { "delay": 1.0, "resonators": { "N": {"level": 4, "health": 98, "distance": 50, "owner": "bb1"},"NE": {"level": 4, "health": 98, "distance": 50, "owner": "bb2"},"E": {"level": 4, "health": 98, "distance": 50, "owner": "bb3"},"SE": {"level": 4, "health": 98, "distance": 50, "owner": "bb4"},"SW": {"level": 4, "health": 98, "distance": 50, "owner": "bb5"},"W": {"level": 4, "health": 98, "distance": 50, "owner": "bb6"},"NW": {"level": 4, "health": 98, "distance": 50, "owner": "bb7" } } }
   { "delay": 0.5, "resonators": { "N": {"health": 90 } } }
   { "delay": 0.4, "resonators": { "N": {"health": 80 } } }
   { "delay": 0.3, "resonators": { "N": {"health": 72 }, "NW": {"health": 20 }, "NE": {"health": 30 } } }
   { "delay": 0.3, "resonators": { "N": {"health": 0 }, "NW": {"health": 0 }, "NE": {"health": 30 } } }
   { "delay": 1.0, "resonators": { "N": {"level": 5, "health": 100, "distance": 20, "owner": "bb8"},"NE": {"level": 5, "health": 100, "distance": 20, "owner": "bb9"} } }
```

# To be tested

UTF-8 interesting Portal names ( a la japanese )

Long, generated .json files

Operations that modify instead of replace values, like "recharge"

Time-integrity of operations

Whether actual JSON objects are being generated ( with or without braces, correct mime types )

Reading the JSON description from stdin, which would allow a generator program to be chained to this program

A "macro" designator that would allow one file to point to another file


# TechTHulu specs as of April 8, 2017

The spec for the project's endpoints and rest addresses are like this. This is enabled when the "legacy" mode is enabled.

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
