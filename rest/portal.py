#!/usr/bin/env python3

### VERY MUCH PYTHON 3 !!!


"""
Library routine for parsing and holding multithreaded Portal objects

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

import logging

import copy

import json



# todo: since a mod has an owner, should make it a class as well, for parallelism sake


# Resonator class... because portals have more than one resonator

class Resonator:

    # ordering is important. Sorry
    valid_positions = [  "N", "NE", "E", "SE", "S", "SW","W", "NW" ]

    def __init__(self, position, portal, log, values=None ):
        # print ("Resonator create: position ",position)
        self.portal = portal
        self.position = position
        self.log = log
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

    def hasinterrupt(self):
        return False

    # sometimes it's nice to have the interesting values as a dict
    def getValues(self):
        v = {}
        v["level"] = self.level
        v["health"] = self.health
        v["distance"] = self.distance
        v["owner"] = self.owner
        return v

    # Compare returns an object noting the differences between the old value and the new.
    # or None if they are the same
    #
    # Also returns a list of action types based on what changed or None
    #
    # Need a static method, because sometimes one or the other is null
    @staticmethod
    def difference(old_p, new_p, log):

#        log.info(" reso difference called ")

#       log.info(" old_p %s ", old_p)

#        log.info(" new_p %s ", new_p)

        diffs = {}
        actions = []

        if old_p == None:

            diffs['level'] = new_p.level
            diffs['health'] = new_p.health
#            diffs['position'] = new_p.position
#            diffs['position-old'] = ""
            #diffs['owner'] = new_p.owner
            #diffs['distance'] = new_p.distance
            actions.append("resonator_add")

        else:
            if new_p.level != old_p.level:
                diffs['level'] = new_p.level
                diffs['level-change'] = new_p.level - old_p.level
                if new_p.level == 0:
                    actions.append("resonator_remove")
                elif new_p.level > old_p.level:
                    actions.append("resonator_upgrade")
                else:
                    actions.append("resonator_remove")
                    actions.append("resonator_upgrade")
            if new_p.health != old_p.health:
                diffs['health'] = new_p.health
                diffs['health-change'] = new_p.health - old_p.health
                if new_p.health < old_p.health:
                    actions.append("attack")
                else:
                    actions.append("recharge")
            # this should never happen, because a reso is defined by position
#            if new_p.position != old_p.position:
#                diffs['position'] = new_p.position
#                diffs['position-old'] = old_p.position
            # 
            if new_p.owner != old_p.owner:
                diffs['owner'] = new_p.owner
                diffs['owner-old'] = old_p.owner
                actions.append("resonator_add")
            if new_p.distance != old_p.distance:
                diffs['distance'] = new_p.distance
                diffs['distance-old'] = old_p.distance

        if len(diffs) == 0:
            return None, None

        return actions, diffs

    # returns TRUE if they are value-wise the same
    # return FALSE if they are the same
    @staticmethod
    def equal(old_r, new_r, log):

        if (old_r == None) and (new_r == None):
            return True
        if (old_r == None) or (new_r == None):
            return False

        if new_p.level != old_p.level :
            return False
        if new_p.health != old_p.health :
            return False
        if new_p.owner != old_p.owner :
            return False
        if new_p.distance != old_p.distance:
            return False

        return True

    # only care about a few things at the moment
    def __str__(self):
        return '"{0}": {{"level": {1}, "health": {2} }}'.format(self.position, self.level, self.health)

    def toLegacyStr(self):
        # print (" grabbing reso string: level ",self.level)
        return '{{"level": {0}, "health": {1}, "position": "{2}"}}'.format(self.level, self.health, self.position)

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

    valid_positions = [  "N", "NE", "E", "SE", "S", "SW","W", "NW" ]
    valid_mods = ["FA","HS-C","HS-R","HS-VR","LA-R","LA-VR","SBUL","MH-C","MH-R","MH-VR","PS-C","PS-R","PS-VR","AXA","T"]
    reso_level_XM = [0.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0 ]

    def __init__(self, id_, log):
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
        self.last_mod_time = time.time()
        self.log = log
        # print("Created a new portal object")  

    # returns a new object of the Portal type
    def dup(self):
        n = Portal(self.id_, self.log)
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
        n.last_mod_time = self.last_mod_time
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
        self.last_mod_time = n.last_mod_time
        self.log = n.log

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



    # returns true or false if the two resonator maps are different
    @staticmethod
    def compare_resonators( rs1, rs2 ):
        for pos, value in rs1.items():
            if Resonator.compare(rs2.get(pos), value) == False:
                return False
        return True

    # This function takes a Json string from the file
    # Returns an object for the next line to read
    def setStatusFile( self, jsonStr, lineNumber ):
        log.verbose("Portal set status: line %d using %s ",lineNumber,jsonStr)

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

        now = time.time()

        if "title" in statusObj:
            t = str(statusObj.get("title"))
            if t != portal.title :
                portal.title = t
                portal.last_mod_time = now

        if "faction" in statusObj:
            t = int(statusObj.get("faction"))
            if portal.faction != t :
                portal.faction = t
                portal.last_mod_time = now


        if "owner" in statusObj:
            t = str(statusObj.get("owner"))
            if t != portal.owner :
                portal.owner = t
                portal.last_mod_time = now

        if "mods" in statusObj:
            t_mods = statusObj.get("mods")
            t_mods.sort()
            if portal.mods != t_mods :
                portal.mods = t_mods
                portal.last_mod_time = now

        if "resonators" in statusObj:
            resonators = statusObj.get("resonators")
            for pos, values in resonators.items():
                r = Resonator(pos, None, None, values  )
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

#        log.verbose ("+++++ object after changes: %s",portal)

        # return value is the amount of delay to add
        delay = 0.0
        if "delay" in statusObj:
            delay = float(statusObj.get("delay"))
        return delay

    # This function takes a Json string
    # changes the object
    # Returns a dict showing what changed
    def setStatusJson( self, statusObj, log ):

        log.debug("Portal set status: using json: %s  ",str(statusObj) )

        is_changed = False
        what_changed = {}
        actions = []

        # print(" parsed JSON, taking lock. Object is: ",statusObj)
        with self.lock:
            portal = self.dup()

#        log.debug("Portal set status: title  " )

        if "title" in statusObj:
            if portal.title != str(statusObj.get("title")):
                is_changed = True
                what_changed["title"] = str(statusObj.get("title"))
                portal.title = str(statusObj.get("title"))

                log.debug(" what changed: title %s",portal.title)

#       log.debug("Portal set status: faction  " )

        if "faction" in statusObj:
            old_faction = portal.faction
            new_faction = int(statusObj.get("faction"))

            if old_faction != new_faction:
                is_changed = True
                what_changed["faction"] = new_faction
                portal.faction = new_faction

                actions = self.addAction(actions, self.getFactionAction(old_faction, new_faction))

                log.debug(" what changed: faction %s",portal.faction)

#        log.debug("Portal set status: owner  " )

        if "owner" in statusObj:
            if portal.owner != str(statusObj.get("owner")):
                is_changed = True
                what_changed["owner"] = str(statusObj.get("owner"))
                portal.owner = str(statusObj.get("owner"))
                self.addAction(actions, "portal_neutralized")
                self.addAction(actions, "portal_captured")

                log.debug(" what changed: owner %s",portal.owner)

#        log.debug("Portal set status: mods  " )

#        if "mods" in statusObj:
#            old_mods = portal.mods
#            new_mods = statusObj.get("mods")
#
#            if sorted(old_mods) != sorted(new_mods):
#                is_changed = True
#                portal.mods = []
                #what_changed["mods"] = []

#                mods = statusObj.get("mods")
#                for mod in mods:
#                    portal.mods.append(mod)
                    #what_changed["mods"].append(mod)

#                actions = self.addAction(actions, self.getModsAction(old_mods, new_mods))

#                log.debug(" what changed: mods %s", str(portal.mods))

#        log.debug("Portal set status: reso  " )

        # compare each-by-each
        # TODO! This does not correctly determine the change in health.
        # It may say that a portal's health or level has changed when it hasn't
        reso_is_changed = False
        reso_what_changed = {}
        if "resonators" in statusObj:
            resonators = statusObj.get("resonators")

            # iterate over everything in the old
            for pos in self.valid_positions:
                ptl = portal.resonators.get(pos, None)
                if ptl:
                    # if not in the new, removed
                    if not pos in resonators:
                        reso_is_changed = True
                        reso_what_changed[pos] = {'level': 0, 'health': 0}
                        portal.resonators.pop(pos)
                        actions = self.addAction(actions, "resonator_remove")

            for pos, values in resonators.items():

                r = Resonator(pos, None, log, values )
                acts, diffs = Resonator.difference( portal.resonators.get(pos,None), r, log)

                # log.debug(" what changed: reso %s value %s",pos,diffs)
                
                if diffs:

                    reso_is_changed = True
                    reso_what_changed[pos] = diffs
                    portal.resonators[pos] = r
                    if acts:
                        for a in acts:
                            actions = self.addAction(actions, a)

            # if we changed the resonators, update the health and level
            # todo: what you really need to do is calculate the health via the
            # status obj and compare it. THIS IS WRONG but not very wrong
            # and, like the resonators, it woudl be nice to show not just the new value but the delta
            if reso_is_changed == True:
                is_changed = True
                what_changed["level"] = portal.getLevel()
                portal.level = portal.getLevel()
                what_changed["health"] = portal.getHealth()
                portal.health = portal.getHealth()
                what_changed["resonators"] = reso_what_changed

#        log.debug("Portal set status: check and set  " )

        # validate the new object through the validator
        if portal.check() == False:
            log.warning (" !!! Bad format after applying delta, ignored ")

        else:
 
            if is_changed:
                # copy the parts that should be copied ( ie, not the lock or create time )
                with self.lock:
                    self.set(portal)

        # log.debug("+++++ object after changes: %s",str(self))

        if is_changed:
            return actions, what_changed
        else:
            return None, None

    # Add an action to the list if it does not exist
    def addAction(self, actions, action):
        if not action in actions:
            actions.append(action)
        return actions

    # Get action from faction change
    #
    # If change from no faction to faction, it was captured
    # If change from faction to no faction, it was neutralized
    # If change from one faction to the other, it was a virus
    #
    def getFactionAction(self, old_faction, new_faction):
        if old_faction == 0:
            return "portal_captured"
        else:
            if new_faction == 0:
                return "portal_neutralized"
            else:
                if old_faction == 1:
                    return "virus_jarvis"
                else:
                    return "virus_ada"

    # Get action from mods change
    #
    # If less mods, then it was a mod_remove
    # If more mods or some mods changed, then it was a mod_add
    #
    def getModsAction(self, old_mods, new_mods):
        if len(new_mods) < len(old_mods):
            return "mod_remove"
        else:
            return "mod_add"

    # This is the "current form" that is mussing a lot of information
    def statusLegacy(self):
        resos = []
        num_entries = 0
        for k, v in self.resonators.items():
            # skip if empty, saving space & time
            # print(" r position ",k," value ",str(v))
            if v.level == 0:
                continue
            num_entries += 1
            resos.append(v.toLegacyStr())
            resos.append(",")
        # have to take off the last comma if more than one item
        if num_entries > 0:
            resos.pop()
        reso_string = ''.join(resos)
        return '{{"controllingFaction": {0}, "health": {1}, "level": {2}, "title": "{3}", "resonators": [{4}]}}'.format( 
            self.faction, self.health, self.level, self.title, reso_string )

    # not legacy! The cool kid way with resonators as a dict
    def __str__(self):

        # shortcut - grey
        if self.level == 0:
            return '{{"faction": 0, "health": 0, "level": 0, "title":"{0}","resonators": {{}}, "mods": [] }}'.format(self.title)

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

        mods = []
        howmany = 0
        for v in self.mods:
            mods.append('"')
            mods.append(v)
            mods.append('"')
            mods.append(',')
            howmany += 1
        if howmany > 0:
            mods.pop()
        mod_string = ''.join(mods)

        return '{{"faction": {0}, "health": {1}, "level": {2}, "title": "{3}", "resonators": {{{4}}}, "mods": [{5}] }}'.format( 
            self.faction, self.health, self.level, self.title, reso_string, mod_string )

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

