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
from random import randint
from time import sleep
from celery import Celery
 

COUNTER = 0
 
app = Celery('flower_web', backend ='redis://localhost:6379/1', broker='redis://localhost:6379/0')

@app.task
def dummy_task(arg1, arg2):
    global COUNTER
    rtime = randint(1,5)
    sleep(rtime)
    COUNTER += 1
    return (arg2, COUNTER, rtime)
