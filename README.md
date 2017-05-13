This is the repo for software to control the Magnus Flora Ingress portal installation.

Project proopsal available at https://docs.google.com/document/d/17XLal8pJIuKS8zbrbEbMBsW1uKg1uqn85zSA8VpAoqE/

Google Doc for accessing test hardware: https://docs.google.com/a/bulkowski.org/document/d/1toZWhOTW_NX1vEIn6rs-qxVq4PiRthPhUmPCC9ctM3I/edit?usp=sharing

# Hello !

Welcome to the Silicon Valley Enlightened's entry into the first Magnus Awakens event.

As we're now coming to the last few days of build, I thought it would be great to update the core readme of the code repo to explain the structure.

## SIM

If you're here for the Tecthulu Sim, please CD into the sim directory.

The sim is written ( rather fugly ) to the new Python 3 `asyncio` framework. The benefit is code becomes
simpler, if you're use to programming in something like Node that is inherently async.

For a device like the Raspberry PI3, which has 4 cores, having a core per server with rest interfaces
is a pretty snazzy system.

The install instructions we used for getting Python 3.6.1 and `aiohttp` on all our Raspberry Pi's
are in the sim directorie's readme. But generally it is like this:

- Install PyEnv ( we perhaps should have used VirtualEnv but we didn't )
- Install Python 3.6.1 through virtualenv and set 3.6.1 as your global pyenv
- Use `pip` to install `cchardet aiodns aiohttp`

Then, you can easily run simulatior files.

## Jarvis

Jarvis is the module that polls the Techtulu. It also uses aiohttp, and it converts game
state logic into a REST interface, and calls whatever REST service want to know the answers.

However, we have lots of people in this project, and some like Celery for async programming.
Thus, Jarvis will also be able to put Celery messages on Celery queues. 

Jarvis is also where we will handle any lingering incompatibilities, because Niantic has not provided
us with the necessary information about the interface. Even today that are changing things a bit,
rumoring adding things like usernames and passwords. Fun !


## rest

The Sound and LED services run on rest. There are separate 'sound.py' and 'led.py' in the rest
directory, and there are explainations there of how they work and their peculiarities.

# Contact

Tech contact for this project is `brian@bulkowski.org`. The coders to the project are best looked up
by seeing who contributed !



