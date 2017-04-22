#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
This will 
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

from random import randint
from time import sleep
from celery import Celery
 
COUNTER = 0
 
app = Celery('flower_web', backend ='redis://localhost:6379/1', broker='redis://localhost:6379/0')

# Location is a string with the compas point
# mods is a list of the current mods, not the delta
# level is 0-8 ( integer )
# faction is 0 , 1, 2 ( integer )
# status update gives an entire status object
# tim is a double with time since epoch

@app.task
def status_update( tim, status_obj ):
	pass

@app.task
def sound_change_mods( mods ):
	return

@app.task
def sound_deploy_reso( location, faction, level):
	return

@app.task
def sound_destroy_reso( location ):
	return


@app.task
def dummy_task(arg1, arg2):
    global COUNTER
    rtime = randint(1,5)
    sleep(rtime)
    COUNTER += 1
    return (arg2, COUNTER, rtime)
