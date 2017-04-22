#!/usr/bin/env python3

### VERY MUCH PYTHON 3 !!!


"""
Example for aiohttp.web basic server
Uses a background timer to read from a file to update a shared datastructure
Because it's going to be used as a simulator

Made available under the MIT license as follows:

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
import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

import threading
import time
import datetime
import os

import itertools
import copy

import json


# todo: since a mod has an owner, should make it a class as well, for parallelism sake


# Resonator class... because portals have more than one resonator

class Resonator:

    valid_positions = [ "E", "NE", "N", "NW", "W", "SW", "S", "SE" ]

    def __init__(self, position, values=None ):
        # print ("Resonator create: position ",position)
        self.position = position
        if values == None:
            self.level = 0
            self.health = 0
            self.distance = 0
            self.position = position
            self.owner = ""
        else:
            self.level = int(values.get("level",0))
            self.health = int(values.get("health",0))
            self.distance = int(values.get("distance",0))
            self.owner = str(values.get("owner", ""))

        # print ("Resontaor level: ",self.level)

    def check(self):
        if type(self.level) is not int:
            print("bad level type ",type(self.level))
            return False
        if self.level < 0 or self.level > 8:
            print("bad level value ",self.level)
            return False
        if type(self.health) is not int:
            print("bad level health type ",type(self.health))
            return False
        if self.health < 0 or self.health > 100:
            print("bad level value ",self.health)
            return False
        if type(self.position) is not str:
            print("bad position type ",type(self.position))
            return False
        if self.position not in self.valid_positions:
            print("bad position: ",self.position)
            return False
        if type(self.distance) is not int:
            print("bad distance type ",type(self.distance))
            return False
        if self.distance < 0 or self.distance > 100:
            print("bad distance value ",self.distance)
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

    # without the position, sometimes that is implied 
    def toBetterStr(self):
        if self.level == 0:
            return'"{0}": {{"level": {1} }}'.format(self.position, self.level)
        else:
            return '"{0}": {{"level": {1}, "health": {2}, "distance": {3} }}'.format(self.position, self.level, self.health, self.distance)

# WARNING! This class has multithreaded access.
# Before you access the data structure, grab the lock and release afterward
# do not do anything blocking under the lock
class Portal:

    valid_positions = [ "E", "NE", "N", "NW", "W", "SW", "S", "SE" ]
    valid_mods = ["FA","HS-C","HS-R","HS-VR","LA-R","LA-VR","SBUL","MH-C","MH-R","MH-VR","PS-C","PS-R","PS-VR","AXA","T"]
    reso_level_XM = [0.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0 ]

    def __init__(self, id_, verbose):
        self.faction = 0
        self.health = 0
        self.level = 0
        self.id_ = id_
        self.title = "default portal"
        self.owner = ""
        self.owner_id = 0
        self.resonators = { }
        self.links = []
        self.mods = []
        self.lock = threading.Lock()  
        self.create_time = time.time()
        self.verbose = verbose
        # print("Created a new portal object")  

    # returns a new object of the Portal type
    def dup(self):
        n = Portal(self.id_, self.verbose)
        n.faction = self.faction
        n.health = self.health
        n.level = self.level
        n.title = self.title
        n.owner = self.owner
        n.owner_id = self.owner_id
        if self.resonators:
            n.resonators = self.resonators
        if self.links:
            n.links = self.links
        if self.mods:
            n.mods = self.mods
        n.lock = None
        n.create_time = self.create_time
        # print("Created a duplicate portal object")  
        return n

    # carefully avoid the lock and the creattime
    # otherwise we're copying the object into the self
    # no return
    def set(self, n):
        self.faction = n.faction
        self.health = n.health
        self.level = n.level
        self.title = n.title
        self.owner = n.owner
        self.owner_id = n.owner_id
        self.resonators = n.resonators
        self.links = n.links
        self.mods = n.mods
        self.verbose = n.verbose

    # Health is calculated from resonators states so it is always correct
    def getLevel(self):
        if self.resonators == None:
            return 0
        level_sum = 0
        for k,v in self.resonators.items():
            level_sum += v.level
        return int (level_sum / 8)

    # health is in .... ???
    # Let's try average of the health of the resonators
    def getHealth(self):
        if self.resonators == None:
            return 0
        if len(self.resonators) == 0:
            return 0
        xm_max = 0.0
        xm = 0.0
        for k,v in self.resonators.items():
            reso_xm = self.reso_level_XM[v.level]
            xm_max += reso_xm
            xm += (float(v.health) / 100.0) * reso_xm
        if xm < 0.00001:
            return 0
        r = int ((xm / xm_max) * 100.0)
        if r > 100:
            r = 100
        return r


    # This function takes a Json object
    # Returns an object for the next line to read
    def setStatus( self, jsonStr ):
        if self.verbose:
            print("Portal set status: using: ",jsonStr)

        try:
            statusObj = json.loads(jsonStr)
        except Exception as ex:
            template = "Exception in Portal parsing the json string {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print( message )
            return None

        # print(" parsed JSON, taking lock. Object is: ",statusObj)
        with self.lock:
            portal = self.dup()

        if "title" in statusObj:
            portal.title = str(statusObj.get("title"))

        if "faction" in statusObj:
            portal.faction = int(statusObj.get("faction"))

        if "owner" in statusObj:
            portal.owner = str(statusObj.get("owner"))

        if "mods" in statusObj:
            portal.mods = []
            mods = statusObj.get("mods")
            for mod in mods:
                portal.mods.append(mod)

        if "resonators" in statusObj:
            resonators = statusObj.get("resonators")
            for pos, values in resonators.items():
                r = Resonator(pos, values)
                portal.resonators[pos] = r

            # if we changed the resonators, update the health and level
            portal.level = portal.getLevel()
            portal.health = portal.getHealth()

        # validate the new object through the validator
        if portal.check() == False:
            print (" !!! Bad format after applying delta, line ",lineNumber," ignored ")

            print (" delta which will not be applied: ", str(portal) )

        else:
            # copy the parts that should be copied ( ie, not the lock or create time )
            with self.lock:
                self.set(portal)

        if self.verbose:
            print ("+++++ object after changes: ",str(portal))

        # return value is the amount of delay to add
        delay = 0.0
        if "delay" in statusObj:
            delay = float(statusObj.get("delay"))
        return delay

    # not legacy! The cool kid way with resonators as a dict
    def __str__(self):

        # shortcut - grey
        if self.level == 0:
            return '{{"faction": 0, "health": 0, "level": 0, "title":{0}, "resonators": {{}}, "mods": {{}} }}'.format(self.title)

        #longcut
        howmany = 0
        resos = []
        for k, v in self.resonators.items():
            # skip if empty, saving space & time
            if v.level == 0:
                continue
            howmany += 1
            resos.append(v.toBetterStr())
            resos.append(",")
        if (howmany > 0):
            resos.pop()
        reso_string = ''.join(resos)
        return '{{"faction": {0}, "health": {1}, "level": {2}, "title": "{3}", "resonators": {{{4}}}, "mods": {5} }}'.format( 
            self.faction, self.health, self.level, self.title, reso_string, str(self.mods) )

    # this method makes sure the status is valid and reasonable ( no values greater than game state )
    def check(self):
        if type(self.faction) is not int:
            print("Portal faction type initvalid, is ",type(self.faction))
            return False
        if self.faction < 0 or self.faction > 2:
            print("Illegal Portal faction value ",self.faction)
            return False
        if type(self.health) is not int:
            print("Portal health type invalid, is ",type(self.health))
            return False
        if self.health < 0 or self.health > 100:
            print("Illegal Portal health value ",self.health)
            return False
        if type(self.level) is not int:
            print("Portal level type invalid, is ",type(self.level))
            return False
        if self.level < 0 or self.level > 8:
            print("Illegal Portal level value ",self.level)
            return False
        if type(self.title) is not str:
            print("Portal title type invalid, is ",type(self.title))
            return False
        if len(self.title) > 300:
            print("Portal title seems too long")
            return False
        if type(self.resonators) is not dict:
            print("Portal resonator type wrong, is ",type(self.resonators))
            return False
        if len(self.resonators) > 8:
            print("Portal has incorrect number of resonators ",len(self.resontaors))
            return False
        for k,v in self.resonators.items():
            if k not in self.valid_positions:
                print("resonator has invalid position ",k)
                return False
            if v.check() == False:
                print(" resonator ",v," is not valid ")
                return False
        if type(self.mods) is not list:
            print("Mods wrong type, is ",type(self.mods))
            return False
        if len(self.mods) > 4:
            print("too many mods")
            return False
        for m in self.mods:
            if type(m) is not str:
                print (" type of one of the mods is wrong, is ",type(m))
                return False
            if m not in self.valid_mods:
                print ("invalid mod ",m)
                return False
        return True


