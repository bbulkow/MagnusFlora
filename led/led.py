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

The above copyright notice and this permission notice shall be included in all copies or 
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
from threading import Thread

import logging

import json
import argparse
import pprint

import asyncio
import textwrap

# things that led controllers want
# Control the LEDs of the Magnus Flora portal art display
import opc
from ledlib.helpers import usage, debugprint, verboseprint
from ledlib.ledmath import *
from ledlib.flower import LedPortal, LedAction
from ledlib import globalconfig
from ledlib import globaldata

from ledlib.colordefs import *
from ledlib import portalconfig                 # base/demo state of portal
from ledlib import patterns

from ledlib.opcwrap import start_opc, ledwrite
from ledlib import opcwrap

from aiohttp import web

# import local shared code
from ledlib.portal import Resonator, Portal

# A simple example of a timer function
async def timer(app):

    period = 5.0

    log = app['log']
    log.info(" started timer routine, running every %f seconds",period)

    while True:
        log.info(" hello says the timer! ")

        # read the portal file, for example?
        
        await asyncio.sleep(period)        

#
# A number of debug / demo endpoints
# Note to self: you create a "Response" object, thn
# you manipulate it.
#

# this needs UTF8 because names might have utf8
async def portal_notification(request):

    log = request.app['log']
    ledPortal = request.app['ledportal']
    try:

        # log.debug(" received notification: %s of type %s",request.method, request.content_type)

        req_obj = await request.json()

        action, action_parm = req_obj.get("action", None)
        what_changed = req_obj.get("what_changed", None)
        status_str = req_obj.get("status", None)

#        log.warning(" action: %s on: %s",action, action_parm )
#        log.warning(" what changed: {0}".format(what_changed))

        # update the portal to the newest values
        status_obj = json.loads ( status_str )
        ledPortal.setStatusJsonSimple( status_obj, log )

        # take the action in question
        ledPortal.action(action,action_parm)    

        r = web.Response(text="OK" , charset='utf-8')

    except Exception as e:
        log.warning(" exception while handing portal notification: %s ",str(ex))
        r = web.Response(text="FAIL")

    return r
    

async def hello(request):
    return web.Response(text="Welcome to Magnus Flora Led!")

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
    logger = logging.getLogger('MF_Led')
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
    # app['portal'] = Portal(1, app['log'])

    # background tasks are covered near the bottom of this:
    # http://aiohttp.readthedocs.io/en/stable/web.html
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return 

def led_init(args, g_config, log):


    # command line flags
    globalconfig.debugflag = False
    globalconfig.verboseflag = False
    globalconfig.fastwake = False
    globalconfig.log = log

    globaldata.ledcontrol = start_opc()



    # Start a thread to asynchronously push the pixel array to the LEDs
    let_there_be_light = Thread(target=opcwrap.ledwriteloop)
    let_there_be_light.start()
    log.debug ("Let there be light!")

    # Wake up the whole portal - can take a long time unless fastwake
    # todo: this should be turned into something else but I want to see SOMETHING
    patterns.wake_up (0, globaldata.total_pixels, globaldata.basecolor)
    log.debug ("... and there was light.")

   # load the JSON file if it's around
    portal_json = ""

    try:
        with open(g_config["portalfile"]) as data_file:    
            portal_json = json.load(data_file)
    except Exception as ex:
        log.warning(" initial json file %s does not exist or can't be parsed: %s", g_config["portalfile"], str(ex))
        pass

    # this is the key class that has worker threads and everything,
    # it'll get put onto the app soon
    ledportal = LedPortal(portal_json, log)

    log.info(" initial state, level is %d", ledportal.getLevel() )
    log.info(" initial state, resos are %s", str(ledportal.resonators) )
    for key, value in ledportal.ledResonators.items():
        log.debug(" initial state: LedReso %s is %s", key, value )

    # send the init action to all the petals
    # this is now ASYNC so you should see all work together
    a = LedAction('init')
    for r in Resonator.valid_positions:
        ledportal.ledResonators[r].do_action(a)

    globaldata.ledportal = ledportal


    # print ("writing ", finalcolor, " to the LEDs.")
    # pixels = [ finalcolor ] * numLEDs

    # ledwrite (ledcontrol, pixels)

    return 



# Parse the command line options

parser = argparse.ArgumentParser(description="MagnusFlora Led", fromfile_prefix_chars='@')
parser.add_argument('--config', '-c', help="JSON file with configuration", default="config.json", type=str)
parser.add_argument('--log', help="location of the log file", default="led.log", type=str)
parser.add_argument('--debug', '-d', help=" debug level: CRITICAL ERROR WARNING INFO DEBUG", default="INFO", type=str)

parser.add_argument('--color', type=check_COLOR, help="Named color, can be overridden piecewise.")
parser.add_argument('--red', type=check_RGB)
parser.add_argument('--green', type=check_RGB)
parser.add_argument('--blue', type=check_RGB)
parser.add_argument('--north', dest='north', type=check_RESO, help="From 0 to 7, which reso is north?")

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
log.info('starting MagnusFlora Led: there will be %d cakes', 9 )

# init including the OPC server connectors & remapping
led_init(args, g_config, log)

print("starting MagnusFlora Led monitoring ",g_config["portalfile"]," on port ",g_config["led_port"])

# register all the async stuff
loop = asyncio.get_event_loop()

app = web.Application()
app['config'] = g_config
app['log'] = log
app['ledportal'] = globaldata.ledportal

loop.run_until_complete(init(app, args, loop))

# run the web server
web.run_app(app, port=g_config["led_port"])
