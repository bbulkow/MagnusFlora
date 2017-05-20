#!/usr/bin/env python3

### VERY MUCH PYTHON 3 !!!


"""
Example for aiohttp.web basic async service
Uses a background timer to print to a logger
exposes an obvious REST endpoint
It's a template!

Made available under the MIT license as follows:

Copyright 2017 Brian Bulkowski brian@bulkowski.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice aasyncnd this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import sys
py_ver = sys.version_info[0] + ( sys.version_info[1] / 10.0 )
if py_ver < 3.5:
    raise "Must be using Python 3.5 or better"

import threading
import time
import datetime
import os

import logging

import json
import argparse

import asyncio
import functools
import textwrap

from aiohttp import web

# import local shared code
from portal import Resonator, Portal

import wave
import subprocess

import platform

# should do something less dumb, like checking if a file exists
# instead of coding in something like this
if (platform.system() == 'Darwin'):
    command_filename_offset = 1
    command_template = [ "afplay" ]
elif (platform.system() == 'Linux'):
    command_filename_offset = 1
    command_template = [ "aplay" ]
else:
    print ( "unknown operating system, can't play sounds ")
    sys.exit(0)

# !!!
# Hopefully you will find a way to play both foreground and background
#

# play a sound start, and allow killing
def play_sound_start( filename ):
    global command_template
    global command_filename_offset

    stat = os.stat( filename )

    # let's check the length, in time
    wf = wave.open(filename, 'rb')
    bytes_per_second = wf.getnchannels() * wf.getframerate() * wf.getsampwidth()
    secs = stat.st_size / bytes_per_second
    log.debug ("play sound start: seconds is: ",sec)

    ct = list(command_template)
    ct.insert(command_filename_offset, filename)
    log.debug("play sound start: passing to popen: ", ct)
    proc = subprocess.Popen( ct )

#   print (" delaying ")
#   time.sleep( sec - 1.0 )
#   time.sleep( 2.0 )

    # test: kill the sound, todo, pass back an object that can respond to a kill
    return proc, secs

def play_sound_end( proc ):
    proc.kill()

# if a sound is older than this, it would be confusing to play it, ignore it
maximum_age = 45.0


def switch_sound_cb(i_sound, sequence):

    global maximum_age

    log.info( " switch_sound_cb called ")

    # check for duplicates which is legal
    if (i_sound.sequence != sequence):
        log.warning(" received duplicate call later %d ignoring ", sequence)
        return

    log.warning(" killing old sound, sequence %d ",sequence)
    if (i_sound.event_audio_obj):
        play_sound_end(i_sound.event_audio_obj)
        i_sound.clean()

    log.warning(" start background, or play from queue? ")

    # nothing, play background
    if i_sound.q.empty() :
        i_sound.play_background()
        return

    # something on queue, play it
    while True:
        try:
            s_event = i_sound.q.get_nowait()
        except asyncio.queues.QueueEmpty:
            # drained queue: play background: exit
            log.warning(" ignored all elements on queue, play background ")

            i_sound.play_background()
            return
            
        # if ancient, drop
        if (s_event.received_time + maximum_age < time.time() ):
            log.warning(" ignoring sound too long on queue ")
            continue

        i_sound.play_sound_immediate(s_event)


# the kind of thing that should be on the queue
class SoundEvent:
    def __init__(self, action, received_time):
        self.action = action
        self.received_time = received_time

class IngressSound:

#    actions_info = {
#        'portal_neutralized': [ '../audio/portal_neutralized.wav', 2.0 ],
#        'portal_captured': [ '../audio/portal_online.wav', 4.0 ],
#        'resonator_add': [ '../audio/resonator_deployed.wav', 3.0 ],
#        'resonator_remove': [ '../audio/resonator_destroyed.wav', 2.0],
#        'attack': [ '../audio/under_attack.wav', 3.0 ],
#    }

    actions_sounds_test = {
        'portal_neutralized': [ '../audio/test/scream.wav', 2.0 ],
        'portal_captured': [ '../audio/test/portal_captured_by_RES.wav', 4.0 ],
        'resonator_add': [ '../audio/test/resonator_deployed.wav', 3.0 ],
        'resonator_remove': [ '../audio/test/exterminate.wav', 2.0],
        'resonator_upgrade': [ '../audio/test/resonator_upgraded.wav', 2.0],
        'mod_added': [ '../audio/test/mod_added.wav', 2.0],
        'mod_destroyed': [ '../audio/test/mod_destroyed.wav', 2.0],
        'attack': [ '../audio/test/attack.wav', 3.0 ],
        'recharge': [ '../audio/test/recharged.wav', 3.0],
        'virus_ada': [ '../audio/test/ada.wav', 3.0],
        'virus_jarvis': [ '../audio/test/jarvis.wav', 3.0],
    }

    background_sounds_test = [
        '../audio/violin-test-PCM16.wav' ]


    actions_sounds_prod = {
        'portal_neutralized': [ '../audio/portal_neutralized.wav', 3.0 ],
        'portal_captured': [ '../audio/portal_online.wav', 6.0 ],
        'resonator_add': [ '../audio/resonator_deployed.wav', 3.0 ],
        'resonator_remove': [ '../audio/resonator_destroyed.wav', 3.0],
        'resonator_upgrade': [ '../audio/test/resonator_upgraded.wav', 2.0],
        'mod_added': [ '../audio/mod_deployed.wav', 2.0],
        'mod_destroyed': [ '../audio/mod_destroyed.wav', 2.0],
        'attack': [ '../audio/under_attack.wav', 3.0 ],
        'recharge': [ '../audio/test/recharged.wav', 3.0],
        'virus_ada': [ '../audio/test/virus_ada_refactor.wav', 3.0],
        'virus_jarvis': [ '../audio/virus_jarvis_vocal.wav', 3.0],
    }

    background_sounds_prod = [
        '../audio/magnus_the_song.wav' ]

    legal_actions = [ "attack", "recharge", "resonator_add", "resonator_remove", 
        "portal_neutralized", "portal_captured",
        "mod_added", "mod_destroyed", "resonator_upgrade", "virus_jarvis", "virus_ada"
    ]

    def __init__(self, app):
        self.event_audio_obj = None
        self.event_audio_start = 0.0
        self.event_audio_minimum = 0.0
        self.event_audio_maximum = 0.0
        self.app = app
        self.sequence = 0
        self.background = False # set to true if playing a background sound
        self.action = ""   # the action type if something is playing
        self.actions_sounds = app['actions_sounds']
        self.background_sounds = app['background_sounds']
        self.log = app['log']

        # the queue will hold some number of sounds, too many gets too far behind
        self.q = asyncio.Queue(maxsize=20)

    def clean(self):
        self.event_audio_obj = None
        self.event_audio_start = 0.0
        self.event_audio_minimum = 0.0
        self.event_audio_maximum = 0.0
        self.background = False
        self.action = ""   

    # only to be used if you know nothing is currently playing
    def play_sound_immediate(self, action):

        ainfo = self.actions_sounds.get(action)

        # play new
        self.event_audio_obj, secs = play_sound_start( ainfo[0] )       
        self.event_audio_start = now
        self.event_audio_minimum = now + ainfo[1]
        self.event_audio_maximum = now + secs
        self.action = action
        self.sequence += 1

        # register a callback to switch
        self.log.info(" play immediate: scheduling callback for switch_sound %f seconds from now",secs)
        loop = self.app['loop']
        loop.call_later(secs, switch_sound_cb, self, self.sequence)

	# action is a string, one defined in the doc:
	# attack, recharge, resonator_add, resonator_remove, portal_neutralized, portal_captured, 
	# mod_added, mod_destroyed, resonator_upgrade, jarvis, ada

    def play_action(self, action ):

        self.log.info(" play_action:  %s",action)

        if action not in IngressSound.legal_actions:
            self.log.warning(" received illegal action, ingoring, %s",action)
            return

        self.log.info(" received valid action: %s",action)
        self.log.debug(" action sounds struct: %s",self.actions_sounds)
        ainfo = self.actions_sounds.get(action, None)
        if ainfo == None:
            self.log.warning(" received unsupported action, ignoring, %s",action)
            return
        self.log.debug(" ainfo %s",ainfo)

        # special case: for attack and defend, ignore multiples
        if (action == "attack" or action == "defend"):
            if self.action == action:
                self.log.warning(" ignoring duplicate %s sound ",action)
                return

        now = time.time()

        # if old one playing, kill it
        if (self.event_audio_obj):
            if (self.background):
                self.log.info(" killing background ")
                play_sound_end(self.event_audio_obj)
                self.clean()

            elif (now > self.event_audio_minimum):
                self.log.info(" killing old sound ")
                play_sound_end(self.event_audio_obj)
                self.clean()

            else:
                self.log.info(" queing sound: %s %f",action,now)
                queue = self.q
                queue.put_nowait( SoundEvent(action, now ) )
                return
	
        # play new
        self.event_audio_obj, secs = play_sound_start( ainfo[0] )		
        self.event_audio_start = now
        self.event_audio_minimum = now + ainfo[1]
        self.event_audio_maximum = now + secs
        self.action = action
        self.sequence += 1

        # register a callback to switch
        self.log.info(" playing sound, and scheduling callback for switch_sound %f seconds from now",secs)
        loop = self.app['loop']
        loop.call_later(secs, switch_sound_cb, self, self.sequence)

    def play_background(self):

        #
        self.log.info(" PLAY BACKGROUND SOUND")

        now = time.time()
        self.event_audio_obj, secs = play_sound_start( self.background_sounds[0] )     
        self.event_audio_start = now
        self.event_audio_minimum = now
        self.event_audio_maximum = now + secs
        self.sequence += 1

		# register a callback to switch
        self.log.info(" background: scheduling callback for switch_sound %f seconds from now",secs)
        loop = self.app['loop']
        loop.call_later(secs, switch_sound_cb, self, self.sequence)



# play a sound start, and allow killing
def play_sound_start( filename ):
    global command_template
    global command_filename_offset

    stat = os.stat( filename )

    # let's check the length, in time
    wf = wave.open(filename, 'rb')
    bytes_per_second = wf.getnchannels() * wf.getframerate() * wf.getsampwidth()
    sec = stat.st_size / bytes_per_second

    ct = list(command_template)
    ct.insert(command_filename_offset, filename)
    proc = subprocess.Popen( ct )

#   print (" delaying ")
#   time.sleep( sec - 1.0 )
#   time.sleep( 2.0 )

    # test: kill the sound, todo, pass back an object that can respond to a kill
    return (proc, sec)

def play_sound_end( proc ):
    proc.kill()


# A simple example of a timer function
async def timer(app):

    period = 5.0

    log = app['log']
    log.info(" started timer routine, running every %f seconds",period)

    while True:
        log.debug(" hello says the timer! ")

        # read the portal file, for example?
        
        await asyncio.sleep(period)        

#
# A number of debug / demo endpoints
# Note to self: you create a "Response" object, thn
# you manipulate it.
#

# this needs UTF8 because names might have utf8
# 
# ENTRY POINT where Jarvis calls me
#
async def portal_notification(request):

    log = request.app['log']
    sound = request.app['sound']
    try:

        log.debug(" received notification: %s of type %s",request.method, request.content_type)

        req_obj = await request.json()
        log.debug(" received JSON %s",req_obj)

        action_str = req_obj.get("action", None)

        log.debug(" action is: %s sound is: %s",action_str, sound)

        sound.play_action(action_str)

        r = web.Response(text="OK" , charset='utf-8')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        # log.warning(" exception while handing portal notification: %s ",str(ex))
        r = web.Response(text="FAIL")


    return r
    

async def hello(request):
    return web.Response(text="Welcome to Magnus Flora Sound! Please replace me.")

async def health(request):
    return web.Response(text="OK")


# background tasks are covered near the bottom of this:
# http://aiohttp.readthedocs.io/en/stable/web.html
# Whatever tasks you create here will be executed and cancelled properly

async def start_background_tasks(app):
    app['timer_task'] = app.loop.create_task( timer(app) )

async def cleanup_background_tasks(app):
    app['log'].info(" cleaning up background tasks ")
    app['timer_task'].cancel()
    await app['timer_task']

def create_logger(args):
    # create a logging object and add it to the app object
    logger = logging.getLogger('MF_Sound')
    logger.setLevel(args.debug)
    # create a file output
    fh = logging.FileHandler(args.log)
    fh.setLevel(args.debug)
    # create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(args.debug)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


async def init(app, args, loop):

    app.router.add_get('/', hello)
    app.router.add_get('/health', health)

    app.router.add_post('/portal', portal_notification)

    # create a portal object and stash it, many will need it
    app['portal'] = Portal(1, app['log'])

    # An Object For Sound
    app['sound'] = IngressSound(app)


	# background tasks are covered near the bottom of this:
	# http://aiohttp.readthedocs.io/en/stable/web.html
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return 


# Parse the command line options

parser = argparse.ArgumentParser(description="MagnusFlora Sound")
parser.add_argument('--config', '-c', help="JSON file with configuration", default="config.json", type=str)
parser.add_argument('--log', help="location of the log file", default="sound.log", type=str)
parser.add_argument('--debug', '-d', help=" debug level: CRITICAL ERROR WARNING INFO DEBUG", default="INFO", type=str)
args = parser.parse_args()

# Load config.json
try:
    with open(args.config) as config_file:
        g_config = json.load(config_file)
        print(" g_config is: ",g_config)
except Exception as e:
    print(" UNABLE TO OPEN CONFIGURATION FILE ",args.config)
    print(e)
    sys.exit(0)

log = create_logger(args)
log.info('starting MagnusFlora Sound: there will be %d cakes', 2 )

print("starting MagnusFlora Sound monitoring ",g_config["portalfile"]," on port ",g_config["sound_port"])

# register all the async stuff
loop = asyncio.get_event_loop()

app = web.Application()
app['config'] = g_config
app['log'] = log
app['loop'] = loop

#
if g_config['sound_type'] == 'prod':
    log.info(" Using Sound Type Prod")
    app['actions_sounds'] = IngressSound.actions_sounds_prod
    app['background_sounds'] = IngressSound.background_sounds_prod
elif g_config['sound_type'] == 'test':
    log.info(" Using Sound Type Prod")
    app['actions_sounds'] = IngressSound.actions_sounds_test
    app['background_sounds'] = IngressSound.background_sounds_test
else:
    log.warning(" Sound Type %s NOT SUPPORTED", g_config['sound_type'])
    app['action_sounds'] = None
    app['background_sounds'] = None

loop.run_until_complete(init(app, args, loop))

# run the web server
web.run_app(app, port=g_config["sound_port"])
