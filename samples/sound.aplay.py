import sys

import sounddevice as sd
import soundfile as sff

import wave


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


#reso_destroyed = "../audio/resonator_destroyed1.wav"
#reso_deployed = "../audio/resonator_deployed1.wav"
#test_file = "../audio/violin-test-PCM16-48.wav"
test_file = "../audio/violin-test-PCM16.wav"


CHUNK = 1024 * 16

print("wave open")

wf = wave.open(test_file, 'rb')
print (" wave object: channels ",wf.getnchannels()," rate ",wf.getframerate()," samp width ",wf.getsampwidth() )

duration = 5
device = 0
dtype = 'int16'

with sff.SoundFile(test_file) as sf:
    def callback(outdata, frame_count, time, status):
        data = sf.read(frame_count, dtype=dtype, out=outdata)
        if (data.size != outdata.size): 
            # zero the part of outdata not written into by sf.read()
            outdata[data.shape[0]:,:].fill(0.0)
            raise sd.CallbackStop()

    with sd.OutputStream(device=device, samplerate=sf.samplerate,
                        channels=sf.channels,
                        dtype=dtype,
                        callback=callback) as ss:
        while (ss.active):
            sd.sleep(duration * 1000)



