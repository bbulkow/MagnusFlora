#!/bin/sh
rm portal.json
python jarvis.py &
python led.py &
python sound.py &
python servo.py &