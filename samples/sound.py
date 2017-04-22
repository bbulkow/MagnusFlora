import pyaudio
import wave

reso_destroyed = "../audio/resonator_destroyed1.wav"
reso_deployed = "../audio/resonator_deployed1.wav"

CHUNK = 1024

print("wave open")

wf = wave.open(reso_destroyed, 'rb')

print(" pyaudio create" )

p = pyaudio.PyAudio()

print(" pyaudio open")

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
				channels=wf.getchannels(),
				rate = wf.getframerate(),
				output = True )

print("pyaudio readframes / write")

data = wf.readframes(CHUNK)
while len(data) > 0:
	stream.write(data)
	data = wf.readframes(CHUNK)

stream.stop_stream()

p.terminate()


