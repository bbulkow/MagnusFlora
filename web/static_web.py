#!/usr/bin/env python3

### VERY MUCH PYTHON 3 !!!


"""
Serve up static web pages

For Magnus Flora Demo

(Said static web pages then make ajax requests to jarvis and the simulator. All UI logic resides
on the client)

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
  

#
# A number of debug / demo endpoints
#

async def hello(request):
    return web.Response(text="This is the static webserver.")

async def health(request):
    return web.Response(text="OK")


async def index(request):
    return web.FileResponse('./index.html')

# background tasks are covered near the bottom of this:
# http://aiohttp.readthedocs.io/en/stable/web.html
# Whatever tasks you create here will be executed and cancelled properly


def create_logger(args):
    # create a logging object and add it to the app object
    logger = logging.getLogger('MF_Web_Static')
    logger.setLevel(logging.DEBUG)
    # create a file output
    fh = logging.FileHandler('mf_static.log')
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

    app.router.add_get('/hello', hello)
    app.router.add_get('/health', health)
    app.router.add_get('/', index)
    app.router.add_static('/static', 'static')
    app.router.add_static('/images', 'static/images')

    # stash it where everyone can find it
    app['log'] = logger

    return app

if __name__ == '__main__':
    # Parse the command line options
    parser = argparse.ArgumentParser(description="MagnusFlora Web Static")
    parser.add_argument('--port', '-p', help="HTTP port", default="8080", type=int)
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
