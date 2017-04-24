import sys
import pyaudio
import wave

#reso_destroyed = "../audio/resonator_destroyed1.wav"
#reso_deployed = "../audio/resonator_deployed1.wav"
test_file = "../audio/violin-test-PCM16-48.wav"
#test_file = "../audio/violin-test-PCM16.wav"

CHUNK = 1024 * 16

print("wave open")

wf = wave.open(test_file, 'rb')
print (" wave object: channels ",wf.getnchannels()," rate ",wf.getframerate()," samp width ",wf.getsampwidth() )

print(" pyaudio create" )

try:
	aud = pyaudio.PyAudio()
except:
	print(" pyaudio open failed, threw exception")
	sys.exit()

print(" pyaudio open")

print(" iterate devices")
for index in range(aud.get_device_count()):
	desc = aud.get_device_info_by_index(index)
	print(" audio device: idx ",index," desc ",desc)
	

try:
	stream = aud.open(format=aud.get_format_from_width(wf.getsampwidth()),
				channels=wf.getnchannels(),
				rate = wf.getframerate(),
				frames_per_buffer = wf.getframerate(),
				output = True )
#	stream = aud.open(format=aud.get_format_from_width(wf.getsampwidth()),
#				channels=wf.getnchannels(),
#				rate = wf.getframerate(),
#				output = True )

except Exception as e:
	print("pyaudio open failed, exception ",e)
	sys.exit()

print("pyaudio readframes / write")

data = wf.readframes(CHUNK)
while len(data) > 0:
	stream.write(data)
	data = wf.readframes(CHUNK)

stream.stop_stream()

p.terminate()


