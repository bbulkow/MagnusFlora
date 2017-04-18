#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  led_task.py
#  
#  This module provides a Clery task interface to set specified led states
#  via the Fadecandy server
#  
#  the functions in this module should interact directly with Fadecandy
#  
#  the Celery tasks defined in this module should be intended to be run as the
#  result of a http request, and may use state shared in redis to enable
#  external control of running tasks.
#  
import time
from celery import Celery
import redis
import opc

REDIS = redis.StrictRedis(host='localhost', port=6379, db=0) 

app = Celery('flower_web', backend ='redis://localhost:6379/1', broker='redis://localhost:6379/0')
app.conf.CELERY_ACCEPT_CONTENT = ['pickle', 'json']
app.conf.TASK_SERIALIZER = ['pickle']


class FCInterface():
    '''manages the configuration for a FadeCandy interface'''
    def __init__(self, entity_name, led_count, opc_address):
        self._name = entity_name
        self._count = led_count
        self.state_key = entity_name+'/led_state'
        self.chase_key = entity_name+'/led_run'
        self.opc = opc_address
        
        self.DEBUG = True
        self.set_state('initialized', True)

    @property
    def state(self):
        return REDIS.hgetall(self.state_key)
    
    def set_state(self, key, value):
        REDIS.hmset(self.state_key, {key:value})

# the tasks are defined outside of the class, due to a limitation in Celery
# each task takes an "objIn" argument, which behaves like the 'self' argument
# for instance methods. The serializer argument specifies how the objIn is
# sent into this method from other processes

@app.task(serializer='pickle')
def dochase(objIn, numChase):
    '''an example long-running task with external control. 
    Light each LED in sequence, and repeat.'''
    objIn.set_state("chase","running")
    REDIS.set(objIn.chase_key, 1)
    while REDIS.get(objIn.chase_key) != '0': #redis values come back as strings
        for i in xrange(objIn._count):
            pixels = [ (150,50,50) ] * objIn._count
            # pixels[i] = (5, 5, 155)
            # pool = cycle(pixels)
            for j in xrange(numChase):
                if i+j <= objIn._count:
                    pixels[i+j-1] = (5, 5, 155)
            if objIn.DEBUG:
                print(i+j)
            else:
                objIn.opc.put_pixels(pixels)
            time.sleep(0.3)

@app.task(serializer='pickle')
def stop_chase(objIn):
    '''an example short running task, which modifies shared state'''
    objIn.set_state("chase", "stopped")
    REDIS.set(objIn.chase_key, 0)

@app.task(serializer='pickle')
def get_state(objIn):
    '''an example task with a return value'''
    return objIn.state


#  individual entities must be defined to be passed into the tasks
#  it makes sense to do this in the same file that the tasks are defined in
#  but we could break this out into a new file when we have a lot of entities
PETAL0 = FCInterface('PETAL0', 24, opc.Client('192.168.4.15:7890'))
