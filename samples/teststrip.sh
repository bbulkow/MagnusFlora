#!/bin/bash

# NOTE! This needs to run from supervisord so take nothing for granted

export PYENV_ROOT="/usr/local/bin/pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
sudo pyenv shell 3.6.1
echo `pyenv version`

while true ; do
	cd "/home/pi/brian"
	python fade-fade.py --color r --duration 10
	python fade-fade.py --color g --duration 10
	python fade-fade.py --color b --duration 10
    python fade-fade.py --color w --duration 20

done
