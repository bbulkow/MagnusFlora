import sys
py_ver = sys.version_info[0] + ( sys.version_info[1] / 10.0 )
if py_ver < 3.5:
    raise "Must be using Python 3.5 or better"

import os
import time

# this helps me know how long in time a file will play
import wave

import random

import subprocess


"""
A player of our sounds
Sound files are in our audio directory
This one uses 'Process' and launches outside processes to play sound
on the Rpi that should be 'aplay' which works asyncornizlly and nicely

However you can set different players

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

# why are these lists? Because it's cool to have a selection of different sounds
# this will randomly play one from the list

game_audio_files = {
	'portal_neutralized': [ '../audio/portal_neutralized.wav' ],
	'portal_online': [ '../audio/portal_online.wav' ],
	'reso_deployed': [ '../audio/resonator_deployed.wav' ],
	'reso_destroyed': [ '../audio/resonator_destroyed.wav'],
	'under_attack': [ '../audio/under_attack.wav' ],
}

background_sounds = [
	'../audio/violin-test-PCM16.wav' ]

# insert the filename at the command: so 1 is right after the command
#command_filename_offset = 3
#command_template = [ 'aplay', ' -f','cd' ]
command_filename_offset = 1
command_template = [ "aplay" ]


# returns some kind of object to allow killing
def play_sound_start( filename ):
	global command_template
	global command_filename_offset

	stat = os.stat( filename )

	# let's check the length, in time
	wf = wave.open(filename, 'rb')
	bytes_per_second = wf.getnchannels() * wf.getframerate() * wf.getsampwidth()
	sec = stat.st_size / bytes_per_second
	print ("seconds is: ",sec)

	ct = list(command_template)
	ct.insert(command_filename_offset, filename)
	print(" passing to popen: ", ct)
	proc = subprocess.Popen( ct )

#	print (" delaying ") 
#	time.sleep( sec - 1.0 )
#	time.sleep( 2.0 )

	# test: kill the sound, todo, pass back an object that can respond to a kill
	return proc

def play_sound_end( proc ):
	proc.kill()
	

# Playing sound one and two at the same time, as a test
# Although the RPI has the hardware capability of playing two sounds,
# other things don't. So this is a bad test.
#print( " starting two sounds " )
#s1 = play_sound_start( '../audio/portal_online.wav' )
#s2 = play_sound_start( '../audio/violin-test-PCM16.wav' )

#print ( " listen to the sounds! " )
#time.sleep(10.0)

#print ( " terminating the sounds " )
#play_sound_end( s1 )
#play_sound_end( s2 )

def loop_sounds():


	for key in game_audio_files:
		fl = game_audio_files[ key ]
		if len(fl) == 0:
			continue
		elif len(fl) == 1:
			fn = fl[0]
		else:
			fn = fl[ random.randint(0,len(fl)-1) ]
		print (" playing audio file: ",fn )

		# let's check the length
		wf = wave.open(fn, 'rb')
		print (" wave object: channels ",wf.getnchannels()," rate ",wf.getframerate()," samp width ",wf.getsampwidth() )

		play_sound_start(fn)

loop_sounds()





