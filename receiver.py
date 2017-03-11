'''
Andrew Zhou
Sheng Tan
UC Berkeley
EE 126 Spring 2017 Project

Used Code for receiver function from

http://stackoverflow.com/questions/2648151/python-frequency-detection

http://stackoverflow.com/questions/2668442/detect-and-record-a-sound-with-python

For educational use--school project.
'''


import pyaudio
import wave
import numpy as np

#Write character string to output file
def write_file(str):
    text_file = open("output.txt","w")
    text_file.write(str)
    text_file.close()

#Translate Sound Frequencies into Character Strings
def decode(sound):


def receiver(file):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 2.98
    WAVE_OUTPUT_FILENAME = "output.wav"

    #use a Blackman window
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
if __name__ == '__main__':
    file = readCommand(sys.argv[1])
    receiver(file)
