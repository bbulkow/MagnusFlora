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

import logging

import json
import argparse

import asyncio
import textwrap

from aiohttp import web

# import local shared code
from portal import Resonator, Portal

# A simple example of a timer function
async def timer(app):

    period = 5.0

    logger = app['log']
    logger.info(" started timer routine, running every %f seconds",period)

    while True:
        logger.info(" hello says the timer! ")

        # read the portal file, for example?
        
        await asyncio.sleep(period)        

#
# A number of debug / demo endpoints
# Note to self: you create a "Response" object, thn
# you manipulate it.
#

# this needs UTF8 because names might have utf8
async def portal_notification(request):

    logger = request.app['log']
    try:

        logger.debug(" received notification: %s of type %s",request.method, request.content_type)

        req_obj = await request.json()
        logger.debug(" received JSON %s",req_obj)
        r = web.Response(text="OK" , charset='utf-8')
    except Exception as e:
        logger.warning(" exception while handing portal notification: %s ",str(ex))
        r = web.Response(text="FAIL")

    return r
    

async def hello(request):
    return web.Response(text="Welcome to Magnus Flora Template! Please replace me.")

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
    logger = logging.getLogger('MF_Template')
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

    # background tasks are covered near the bottom of this:
    # http://aiohttp.readthedocs.io/en/stable/web.html
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return 


# Parse the command line options

parser = argparse.ArgumentParser(description="MagnusFlora Template")
parser.add_argument('--config', '-c', help="JSON file with configuration", default="config.json", type=str)
parser.add_argument('--log', help="location of the log file", default="template.log", type=str)
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
logger.info('starting MagnusFlora Template: there will be %d cakes', 2 )

print("starting MagnusFlora Template monitoring ",g_config["portalfile"]," on port ",g_config["template_port"])


# register all the async stuff
loop = asyncio.get_event_loop()

app = web.Application()
app['config'] = g_config
app['log'] = logger

loop.run_until_complete(init(app, args, loop))

# run the web server
web.run_app(app, port=g_config["template_port"])
