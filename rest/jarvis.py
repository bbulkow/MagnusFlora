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
OUT OF OR IN CONNECTION WITH THE SOFTWportARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

import textwrap

from aiohttp import web
import aiohttp
import asyncio
import async_timeout

# import local shared code
from portal import Resonator, Portal

class Notification:
    # app is my app, that has some interesting parameters
    # payload is a string to be delivered JSON style
    # URL is the remote endpoint to notify

    def __init__(self, app, url, payload):
        self.app = app
        self.payload = payload
        self.url = url

    # queueing: if it's full just don't notify
    def enqueue(self):
        q = self.app['queue']
        try:
            q.put_nowait(self)
        except QueueFull:
            logger.warning(" can't queue for notification ")
            pass

    async def notify(self):
        session = self.app['session']
        logger.debug(" Notification: notify posting JSON to endpoint %s",self.url)
        with async_timeout.timeout(1.0):
            headers = {'content-type': 'application/json; charset=utf-8' }
            async with session.post(self.url, data=self.payload) as resp:
            # with session.post(self.url) as resp:
                logger.debug("post notification: response code: %d",resp.status)
                if resp.status != 200:
                    logger.warning(" post: response is not 200, is %d, ignoring",resp.status)
                    return 
        return 

#
# Task that asynchronously polls the Techthulu module
# and looks for changes.
# based on those changes it will notify the different worker units,
# and update the stored file
#

# write the portal to disk - since it's local, do it synchronously
def write_file( filename, portal_str ):
    
    logger.info(" writing file %s string %s",filename,portal_str)

    # open the file, write it
    with open(filename, "w") as f:
        f = open(filename, "w")
        f.write(portal_str)
        f.close()
        
    logger.info(" wrote to file ")

#
# Post to an endpoint
#
async def post_json(session, url, json_str):
    logger.debug(" posting JSON to endpoint %s",url)
    with async_timeout.timeout(2):
        headers = {'content-type': 'application/json; charset=utf-8' }
        async with session.post(url, data=json_str, headers=headers) as resp:
            #logger.debug("fetch: response code: %d",resp.status)
            if resp.status != 200:
                logger.warning(" fetch: response is not 200, is %d, ignoring",resp.status)
                return None
            return await resp.text()


# a template from the docs
# just usef for basic health check ATM
async def fetch(session, url):
    with async_timeout.timeout(2):
        async with session.get(url) as resp:
            #logger.debug("fetch: response code: %d",resp.status)
            if resp.status != 200:
                logger.warning(" fetch: response is not 200, is %d, ignoring",resp.status)
                return None
            return await resp.text()

# Actually make the JSON request to the simulator
# Since this is a co-routine, it can be called blocking or non-blocking
# We will do all the work here of updating the portal and calling the necessary handlers

async def portal_status(session, url, app):

    # get urls to post responses to
    g_config = app["config"]
    driver_urls = []
    for d in g_config["drivers"]:
        driver_urls.append( g_config[d] )

    with async_timeout.timeout(2):
        async with session.get(url) as resp:
            logger.debug(" response code: %s content-type %s",resp.status, resp.headers['Content-Type'])
            if resp.status != 200:
                return None
            resp_type = resp.headers['Content-Type']
            if resp_type.find("text/plain"):
                resp_text = await resp.text()
            elif resp_type.find("application/json"):
                resp_text = await resp.text()
            else:
                logger.warning(" unknown content type %s , will treat as text",resp_type)
                resp_text = await resp.text()

            # important log! What did TecThulu say???
            logger.debug(" status: response text %s",resp_text)
            
            # parse the json object
            try:
                status_obj = json.loads(resp_text)
            except ValueError:
                logger.warning("portal_status: could not decode JSON response string from thulu %s",resp_text)
                return None
            except Exception as ex:
                logger.warning(" could not decode JSON string, exception %s ",str(ex))
                return None

            # logger.debug(" json load success ")

            # Determine if there are differences between the old and new object
            # what_changed is a dict with things that changed
            portal = app['portal']
            # this sets the status and returns what changed
            what_changed = portal.setStatusJson(status_obj, logger)

            # If the object has changed,
            if what_changed:
                logger.info(" something changed! %s ",what_changed)

                # get the encoded string only once
                with portal.lock:
                    portal_str = str(portal)

                logger.debug(" changed: got string %s ",portal_str)

                # write to the file
                write_file(g_config["portalfile"], portal_str)
                logger.debug(" changed:  updated file")

                #    Send a JSON request to the drivers
                logger.debug(" Notifying following clients: drivers %s ",driver_urls)

                for u in driver_urls:
                    n = Notification(app, u, portal_str)
                    n.enqueue()

            else:
                logger.debug(" nothing changed ")

            return status_obj

# work routine that actually polls in a loop
async def thulu_poller(app):


    g_config = app['config']

    period = g_config["tecthulu_poll"]

    logger = app['log']
    logger.info(" started poller routine, running every %f seconds",period)

    # reuse this object, no reason to create lots of them
    async with aiohttp.ClientSession(loop=loop) as session:

        app['session'] = session

        while True:
            logger.info(" hello says the poller! ")

            # todo: don't bother with user agent, other headers? ( skip_auto_headers )
            try:
 #               async with aiohttp.ClientSession(loop=loop) as session:
                html = await fetch(session, g_config["tecthulu_url"])
                logger.debug( "Poller: thulu is up, root received valid response")

                # gets the status and decodes the json into an object
                res = await portal_status(session, 'http://localhost:5050/status/json', app)

            except aiohttp.ClientConnectionError as ex:
                logger.error( "Poller: could not connect to server, reason %s ",ex)

            except asyncio.TimeoutError as ex:
                logger.error( "Poller: timed out fetching from server, trying again ")

            except Exception as ex:
                logger.error( "Poller: unknown exception type %s",type(ex).__name__)

            await asyncio.sleep(period) 


async def timer(app):

    period = 1.0
    logger = app['log']
    # logger.info(" started timer routine, running every %f seconds",period)

    while True:
        # logger.info(" hello says the timer! ")
        await asyncio.sleep(period) 


async def notifier_task(app):
    logger.info(" notifier task started")

    queue = app['queue']
    while True:
        work = await queue.get()
        try:
            await work.notify()
        except Exception as e:
            logger.error(" notification failed, %s",str(e))


#
# A number of debug / demo endpoints
# Note to self: you create a "Response" object, thn
# you manipulate it.
#

# this needs UTF8 because names might have utf8
async def statusJson(request):
    portal = request.app['portal']
    portal_str = ""
    with portal.lock:
        portal_str = str(portal)
    return web.Response(text=portal_str , charset='utf-8')

async def hello(request):
    return web.Response(text="Welcome to Magnus Flora Jarvis Server! Please replace me.")

async def health(request):
    return web.Response(text="OK")


# background tasks are covered near the bottom of this:
# http://aiohttp.readthedocs.io/en/stable/web.html
# Whatever tasks you create here will be executed and cancelled properly

async def start_background_tasks(app):
    app['timer_task'] = app.loop.create_task( timer(app))
    app['poller_task'] = app.loop.create_task( thulu_poller(app))
    app['notifier_task'] = app.loop.create_task( notifier_task(app))

async def cleanup_background_tasks(app):
    app['log'].info(" cleaning up background tasks ")
    app['timer_task'].cancel()
    await app['timer_task']
    app['poller_task'].cancel()
    await app['poller_task']
    app['notifier_task'].cancel()
    await app['notifier_task']

def create_logger(args):
    # create a logging object and add it to the app object
    logger = logging.getLogger('MF_Jarvis')
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

    app.router.add_get('/status/json', statusJson)

    # create a portal object and stash it, many will need it
    app['portal'] = Portal(1, app['log'])

    # worker queue for notifier tasks
    app['queue'] = asyncio.Queue(loop = loop)

    # background tasks are covered near the bottom of this:
    # http://aiohttp.readthedocs.io/en/stable/web.html
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return 

# Parse the command line options

parser = argparse.ArgumentParser(description="MagnusFlora Jarvis")
parser.add_argument('--config', '-c', help="JSON file with configuration", default="config.json", type=str)
parser.add_argument('--log', help="location of the log file", default="jarvis.log", type=str)
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

logger = create_logger(args)
logger.info('starting MagnusFlora Jarvis: there will be %d cakes', 3 )

print("starting MagnusFlora Jarvis on port ",g_config["jarvis_port"])

# register all the async stuff
loop = asyncio.get_event_loop()

app = web.Application()
app['config'] = g_config
app['log'] = logger

loop.run_until_complete(init(app, args, loop))

# run the web server
web.run_app(app, port=g_config["jarvis_port"])
