#!/bin/bash

# this script is used to launch in an environment when you need to run pyenv.
# SupervisorD isn't really good at pyenv. Thus I am hacking this in to make
# launching with PyEnv possible.

export PYENV_ROOT="/usr/local/bin/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

cd /home/pi/MagnusFlora/rest

#python jarvis.py -c config.json -d DEBUG
python jarvis.py -c config.json 


