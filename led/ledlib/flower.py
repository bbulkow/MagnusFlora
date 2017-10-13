# class definitions for the flower as a whole

# TODO: import from rest.portal

from ledlib.portal import Resonator, Portal
from ledlib.helpers import debugprint

from ledlib import patterns
from ledlib import colordefs

from ledlib.colordefs import *


import threading
import logging
import time
# python3 calls it Queue
import queue


class LedPortal(Portal):

    valid_positions = [  "N", "NE", "E", "SE", "S", "SW","W", "NW" ]

    def __init__(self, jsonObj, log):
        # superclass
        Portal.__init__(self,id,log)

        log.debug(" LedPortal initializing !!! ")

        # this will init all the Portal's fields
        if jsonObj != None:
            self.setStatusJsonSimple(jsonObj, log)

        verbose=True

        # create the LedResonators, also make the resonators LedResonattors
        self.ledResonators = {}
        for fc in range(4):                             # 4 FAdecandy boards
            for side in range(2):                       # 2 sets of 4 channels each
                reso_number = fc * 2 + side     # 8 resos
                pos = self.valid_positions[reso_number]
                portal_res = self.resonators.get(pos, None)
                v = None
                if portal_res:
                    v = portal_res.getValues()
                self.ledResonators[pos] = LedResonator(pos, self, fc, side, log, v)
                # by making the objects the same, when we update a resonator,
                # we see it in both. Arguably there should be no LedResonators structure.
                self.resonators[pos] = self.ledResonators[pos]


    # actions come here from the led.py rest service
    # the action strings are defined somewhere. In a document. Which I lost.
    def action(self, action, action_parm):
        self.log.warning(" LedPortal receiving action %s : %s", action, action_parm)

        if action == 'portal_neutralized':
            # flash grey a lot, leave it grey
            for pos, reso in self.ledResonators.items():
                reso.do_action( LedAction( "neutralized" ) )

        elif action == 'portal_captured':
            # flash the new portal flavor, redraw
            for pos, reso in self.ledResonators.items():
                reso.do_action( LedAction( "captured" ) )

        elif action == 'resonator_add':
            # flash the resonator a lot
            reso = self.ledResonators[action_parm]
            reso.do_action( LedAction("add") )

        elif action == 'resonator_remove':
            # flash the resonator a lot leave it grey
            reso = self.ledResonators[action_parm]
            reso.do_action( LedAction("remove") )

        elif action == 'mod_added':
            self.log.debug(" no led action for adding a mod")

        elif action == 'mod_destroyed':
            self.log.debug(" no led action for removing a mod")

        elif action == 'attack':
            # invert the current portal owner
            act = None
            if self.faction == 0:
                self.log.warning("received attack on unowned portal ignoring")
            elif self.faction == 1:   
                act = LedAction("attack", 2)
            elif self.faction == 2:
                act = LedAction("attack", 1)
            if act:
                # route to the particular resonator
                reso = self.ledResonators[action_parm]
                reso.do_action( act )
                

        elif action == 'recharge':
            if self.faction != 0:
                reso = self.ledResonators[action_parm]
                reso.do_action( LedAction("defend", self.faction) )

        elif action == 'virus_ada':
            self.log.debug(" no action yet for virus ada, add one! )")

        elif action == 'virus_jarvis':
            self.log.debug(" no action yet for virus jarvis, add one! ")

        else:
            self.log.warning(" UNKNOWN ACTION STRING %s ",action )
    
        


# Pixelstring
# name
# base
# size
# direction ( for motion? )

class PixelString(object):
    def __init__(self, name, base, size, direction):
        self.name = name
        self.base = base
        self.size = size
        self.direction = direction
        # TODO: validate direction = 1 or -1
        self.pixels = [0] * self.size
        # why didn't I just use reversed() ?
        if direction == 1:
            for i in range (size):
                self.pixels[i] = base + i
        if direction == -1:
            for i in range (size):
                self.pixels[i] = base + size -1 -i

# Input paramters:
#   'fadecandy', which is an integer which is 0, 1, 2, 3
#   side, which is either 0 or 1 ( side of the fade candy )
#
# a base, which was the base of the fadecandy
# self.LOC - a PixelString of Left Outside
# self.CBOT
# self.LIC - left inner
# self.RIC - right inner center?
# self.RB
# self.
# list_of_lists_of_pixel_numbers - all the pixels in the petal

class PixelMap(object):

    def __init__(self, fadecandy, side):
        # TODO: validate side is 0 or 1
        self.base = (512 * fadecandy) + (256 * side)
        channels = [0, 64, 128, 192]        # TODO these should be in math
        # TODO: better way for overrides

        debugprint ((" definining PixelMap: fadecandy ", fadecandy, "side ", side))

        cbase = self.base  + channels[0]
        self.LOC = PixelString ( "LOC", cbase, 43, 1)
        self.__CBOT = PixelString ("CBOT", cbase + 43, 21, -1)

        cbase = self.base + channels[1]
        self.LIC = PixelString ("LIC", cbase, 36, 1)
        self.LB = PixelString ( "LB", cbase+36, 28, -1)

        cbase = self.base + channels[2]
        self.RIC = PixelString ("RIC", cbase, 36, 1)
        self.RB = PixelString ( "RB", cbase+36, 28, -1)

        cbase = self.base + channels[3]
        self.ROC = PixelString ( "ROC", cbase, 43, 1)
        self.__CTOP = PixelString ("CTOP", cbase + 43, 21, -1)

        # center is composed 
        self.CENTER = PixelString("CENTER", 0, 42, 1)
        self.CENTER.pixels = self.__CBOT.pixels + self.__CTOP.pixels

        self.list_of_lists_of_pixel_numbers = [ \
            self.LOC.pixels, \
            self.LIC.pixels, \
            self.CENTER.pixels, \
            self.RIC.pixels, \
            self.ROC.pixels, \
            self.LB.pixels, \
            self.RB.pixels \
            ]

        # "lixel" was originally a typo but it's a great unique tag
        debugprint (" Here comes the list of pixel numbers" )
        debugprint ((self.list_of_lists_of_pixel_numbers))
        debugprint (("Center: ", self.CENTER.pixels))
        debugprint (("LOC: ", self.LOC.pixels))
        debugprint (" Wheee!!!")

class LedAction():
    def __init__(self,action,faction=0):
        self.action = action
        self.faction = faction
        pass
    def __str__(self):
        return "LedAction: action: {0} faction {1}".format(self.action,self.faction)

# AKA a petal
# has a queue and a thread that reads the queue

class LedResonatorThread( threading.Thread):
    # todo: set more things
    def __init__(self,  ledResonator):
        threading.Thread.__init__(self)
        self.ledResonator = ledResonator
        self.log = ledResonator.log

    # sets the leds to the init base state for the current colors
    def init_pattern(self):
        reso = self.ledResonator
        self.log.info(" init pattern: pos %s faction %d level %d ",reso.position, reso.portal.faction,reso.level)
        patterns.parallel_blend(reso.pixelmap.list_of_lists_of_pixel_numbers, \
                        colordefs.colortable_faction[reso.portal.faction], \
                        colordefs.colortable_level[reso.level], \
                        4.0, \
                        20, \
                        reso)
        # test with a little chase, don't really want chase now
        # self.basic_chase_pattern("ww--ww--ww")
        #patterns.chase(reso.pixelmap.list_of_lists_of_pixel_numbers, "ww--ww--ww", -1, reso)


    def flash_pattern(self, faction ):
        reso = self.ledResonator

        self.log.info(" FLASH pattern: faction %d",faction)

        # 10 flashes in 3.0 seconds
        if faction == 0:
            rgb = colortable["NEUTRAL"]
        elif faction == 1:
            rgb = colortable["ENL"]
        elif faction == 2:
            rgb = colortable["RES"]

        patterns.flash(reso.pixelmap.list_of_lists_of_pixel_numbers, rgb, 10, 3.0, reso)


    def basic_chase_pattern(self, maskstring):
        reso = self.ledResonator
        self.log.info(" New basic CHASE pattern %s started.", maskstring)
        patterns.chase(reso.pixelmap.list_of_lists_of_pixel_numbers, maskstring, -1)        # infinite chase

    # each resonator has this thread running
    def run(self):
        q = self.ledResonator.queue
        reso = self.ledResonator # this is myself, for a shortcut
        while True:
            action = q.get()

            self.log.debug( "LedResonator %s faction %d received action %s qsize %d  ",reso.position, \
                reso.portal.faction, str(action),q.qsize() )

            if action.action == "init":
                self.init_pattern()

            elif action.action == "attack":
                # faction is the number-form here - it means the faction that is attacking
                self.flash_pattern(action.faction)
                self.init_pattern()

            elif action.action == "defend":
                # faction is the number form - it is the faction that is defending
                self.flash_pattern(action.faction)
                self.init_pattern()
 
            elif action.action == "remove":
                # now there is nothing
                self.flash_pattern( 0 )
                self.init_pattern()

            elif action.action == "add":
                self.flash_pattern( reso.portal.faction )
                self.init_pattern()

            else:
                self.log.warning( "resonator received unknown command %s",action.action)

            q.task_done() # tells other guy you are complete

            # TODO: add here the background chase, and have it check the queue for new work
            # frequently
            

class LedResonator(Resonator):


    # usage:
    # FC is fadecandy 0,1,2,3 ; side is 0,1 (side of the FC)
    # resos.append(Ledresonator(reso_number, reso_name, fc, side, level, health, faction)

    def __init__( self, position, portal, fc, side, log, values ):

        # superclass init
        Resonator.__init__(self, position, portal, log, values)
        # this sets log, portal, values in the superclass

        self.pixelmap = PixelMap (fc, side)

        # create the queue between this and the execution thread
        self.queue = queue.Queue()

        # may have to fix up argument so self gets to run
        r_thread = self.thread = LedResonatorThread(self)
        r_thread.start()

    def do_action(self,action):
        self.queue.put(action)

    # return FALSE if there is nothing else to do
    # return TRUE if you have something better to do
    def hasinterrupt(self):
        if self.queue.empty() == True:
            # log.info(" resonator %s has nothing better to do",self.position)
            return False
        else:
            self.log.debug(" resonator %s : qsize %d has SOMETHING better to do",self.position,self.queue.qsize() )
            return True

    def __str__(self):
        return '"{0}": {{"level": {1}, "health": {2} }}'.format(self.position, self.level, self.health)



