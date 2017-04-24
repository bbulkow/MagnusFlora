import sys

import sounddevice as sd
import soundfile as sff

import wave

#reso_destroyed = "../audio/resonator_destroyed1.wav"
#reso_deployed = "../audio/resonator_deployed1.wav"
test_file = "../audio/violin-test-PCM16-48.wav"
#test_file = "../audio/violin-test-PCM16.wav"


CHUNK = 1024 * 16

print("wave open")

wf = wave.open(test_file, 'rb')
print (" wave object: channels ",wf.getnchannels()," rate ",wf.getframerate()," samp width ",wf.getsampwidth() )

duration = 5
filename = '20seconds_sine.wav'
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



