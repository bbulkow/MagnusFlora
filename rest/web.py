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


# Polling the simulator to see what has changed

async def timer(app):

    period = 5.0

    logger = app['log']
    logger.info(" started timer routine, running every %f seconds",period)

    while True:
        logger.info(" hello says the timer! ")

        await asyncio.sleep(period)        

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
    logger = logging.getLogger('MF_Web')
    logger.setLevel(logging.DEBUG)
    # create a file output
    fh = logging.FileHandler('template.verbose.log')
    fh.setLevel(logging.DEBUG)
    # create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

#    if args.verbose:
#        ch.setLevel(logging.ERROR)
#    else:
#        ch.setLevel(logging.DEBUG)
    # what format would you like
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

async def init(app, args, logger):
    app = web.Application()

    app.router.add_get('/', hello)
    app.router.add_get('/health', health)

    app.router.add_get('/status/json', statusJson)

    # create the shared objects - pass args around too
    app['filename'] = args.filename

    # stash it where everyone can find it
    app['log'] = logger

    # background tasks are covered near the bottom of this:
    # http://aiohttp.readthedocs.io/en/stable/web.html
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return app

# Parse the command line options

parser = argparse.ArgumentParser(description="MagnusFlora Web")
parser.add_argument('--port', '-p', help="HTTP port", default="8080", type=int)
parser.add_argument('--file', '-f', dest="filename", help="Template File", default="tecthulu.json", type=str)
parser.add_argument('--verbose', '-v', help="Puts Lots of Printing Noise in", action='store_true')
parser.set_defaults(verbose=False)
args = parser.parse_args()

logger = create_logger(args)
logger.info('starting MagnusFlora Webserver: there will be %d cakes', 80 )


# register all the async stuff
loop = asyncio.get_event_loop()
app = loop.run_until_complete(init(web.Application(), args, logger))

# run the web server
web.run_app(app, port=args.port)
