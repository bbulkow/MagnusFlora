#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dummy_task.py
#
#  Copyright 2017 Joel McGrady <mcgradj@vubuntu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import random
from time import sleep
from celery import Celery
from celery.schedules import crontab

COUNTER = 0

## copy this app part completely
app = Celery('flower_web',
    backend ='redis://localhost:6379/1',
    broker='redis://localhost:6379/0')


## use this to set up periodic tasks. there are also functions to do something
## at a given time (sundown, sunrise), rather than at a specificed interval
## copy the whole function and add the tasks you need, being sure to send '.s'
## the call.
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #schedule a call of hello world for every 2 seconds
    sender.add_periodic_task(2, #number of seconds between calls. can be a floating point and less than one
                             random_task.s('hello world'),
                             name='hworld1')

    sender.add_periodic_task(10, #number of seconds between calls. can be a floating point and less than one
                             dummy_task.s('hello', 'world'),
                             name='hworld2')

@app.task
def dummy_task(arg1, arg2):
    '''demonstarates using global state and a random delay in results'''
    global COUNTER
    rtime = random.randint(1,5)
    sleep(rtime)
    COUNTER += 1
    return (arg2, COUNTER, rtime)


@app.task
def random_task(arg1):
    '''this task should return quickly, since there is no induced delay'''
    return (random.randint(1,100), ''.join(random.sample(arg1, len(arg1))))

########################
##
##  install the celery[redis] package via
##
##  pip install -r requirements.txt
##
##  when you're in the projct's directory.
##
##  to start the celery workers defined here
##
##
##  celery -A dummy_task worker -B --loglevel=INFO
##
##
##  this sends log lines to the terminal. there are command line options
##  to use a logfile as well
##
####################
