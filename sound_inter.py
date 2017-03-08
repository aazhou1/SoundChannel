'''

Used Code from

http://stackoverflow.com/questions/2648151/python-frequency-detection

http://stackoverflow.com/questions/2668442/detect-and-record-a-sound-with-python

'''

# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np





CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2.98
WAVE_OUTPUT_FILENAME = "output.wav"

# use a Blackman window
window = np.blackman(CHUNK*2)
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK) 
    frames.append(data)

stream.close()
p.terminate()

i = 0
while i < len(frames):
    data= frames[i]
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/int(RECORD_SECONDS)),\
        data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/CHUNK
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which*RATE/CHUNK
        print "The freq is %f Hz." % (thefreq)
    # read some more data
    i+=1
play=pyaudio.PyAudio()
stream_play=play.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True)
for data in frames: 
    stream_play.write(data)
stream_play.stop_stream()
stream_play.close()
play.terminate()

