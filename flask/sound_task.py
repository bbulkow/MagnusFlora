#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

"""
The sound task will accept Celery messages as a Celery task

It will manage playing files in the background

It will have configuration options to do the following:
- just output to a file some debug print logs
- Use PyAudio, the most common python audio system that works on the macintosh but has some kind of bug on RaspberryPi
- Use PyAlsaAudio, which actually works on the RasperryPi

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

from time import sleep
from celery import Celery
 
app = Celery('flower_web', backend ='redis://localhost:6379/1', broker='redis://localhost:6379/0')

# Location is a string with the compass point
# mods is a list of the current mods, not the delta
# level is 0-8 ( integer )
# faction is 0 , 1, 2 ( integer )
# status update gives an entire status object
# ts is the time at which the event was noticed in JARVIS: a double with time since epoch

@app.task(name='sound_status_update', bind=True)
def sound_status_update( ts, status_obj ):
	print('sound: status update called, time ',ts,' status ',status_obj)
	return

@app.task(name='sound_change_mods', bind=True)
def sound_change_mods( ts, mods ):
	print('sound: change mods, ',ts," mods ",mods)
	return

@app.task(name='sound_deploy_resonator', bind=True)
def sound_deploy_resonator( ts, location, resonator_level, portal_faction, portal_level):
	print("sound: deploy resonator called, ",ts,' location ',location, status_obj)
	return

@app.task(name='sound_deploy_resonator', bind=True)
def sound_destroy_resonator( ts, location, portal_faction, portal_level ):
	print("sound: status destroy resonator called, ",ts,' location ',location,' portal faction ',portal_faction,' portal level ',portal_level)
	return


