#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  flower_web.py
#  
#  This module provides an http interface for launching and managing Celery tasks.
#  
#  The functions defined here should not perform any interaction with servos,
#  LEDS, etc, and instead defer that to a Celery task. These functions should
#  only parse incoming requests' data into the arguments needed to call the
#  intended task.
#  
#  During initial development, I expect that a different route will be added for
#  each desired behavior. 
#  
#

import json
from flask import Flask
import led_task
import dummy_task


app = Flask('flower_web')

## only needed if we need Celery tasks with Flask contexts
#~ app.config.update(
    #~ CELERY_BROKER_URL='redis://localhost:6379',
    #~ CELERY_RESULT_BACKEND='redis://localhost:6379'
#~ )

@app.route('/randomtask', methods=['GET', 'POST'])
@app.route('/randomtask/<random_str>', methods=['GET', 'POST'])
def call_random(random_str=''):
	return json.dumps(dummy_task.random_task.delay(random_str).get())

@app.route('/dummytask', methods=['GET', 'POST'])
def call_dummy():
	dummy_task.dummy_task.delay("hello", "world")
	return 'True'

@app.route('/<entity_name>/chase/start', methods=['GET', 'POST'])
def startchase(entity_name):
    '''example of starting a long running task asychronistically - the
    return from this funciton may be sent before the task is started, and
    most likely before the task completes'''
    led_task.dochase.delay(getattr(led_task,entity_name),4)
    return 'runstart: {}'.format(entity_name)

@app.route('/<entity_name>/chase/stop', methods=['GET', 'POST'])
def stopchase(entity_name):
    '''example of starting a quick-finishing task'''
    led_task.stop_chase.delay(getattr(led_task,entity_name))
    return 'runstop: {}'.format(entity_name)

@app.route('/<entity_name>/state', methods=['GET', 'POST'])
def getstate(entity_name):
    '''example of getting a return from a task. This only works well when
    the task is quick, since this call will block until a return is generated'''
    ma = led_task.get_state.delay(getattr(led_task,entity_name))
    return json.dumps(ma.get())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
