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

freq_to_hex={}
for x in range(0,10):
    freq_to_hex[187.5 *x + 1000] =187.5 *x + 4000

freq_to_hex['A'] = 187.5*11 + 4000 
freq_to_hex['B'] = 187.5*12 + 4000 
freq_to_hex['C'] = 187.5*13 + 4000 
freq_to_hex['D'] = 187.5*14 + 4000 
freq_to_hex['E'] = 187.5*15 + 4000 
freq_to_hex['F'] = 187.5*16 + 4000 

interm = 187.5*10+4000

#Write character string to output file
def write_file(data, filename):
    text_file = open(filename,"w")
    text_file.write(data)
    text_file.close()

#Translate Sound Frequencies into Character Strings
def decode(sounds):

    i = 0 
    start_string = 0
    last_read = 0 
    interm = 187.5*10+4000
    while i < len(sounds):
        if (abs(9000 - sounds[i]) <= 20) and start_string = 0:
            start_string = 1
            last_read = sounds[i]
            i+=1
        elif (start_string == 1) and (abs(interm - sounds[i])<=20):
            i+=1
        elif (start_string != 0):
            if abs(sounds[i]-last_read) <=20



def receiver(file):
    #3-4 readings per bit

    CHUNK = 200
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1
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
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/2),\
            data))*window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        frequencies =[]
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/CHUNK
            frequencies.append(thefreq)
        else:
            thefreq = which*RATE/CHUNK
            frequencies.append(thefreq)
        # read some more data
        i+=1
    characters = decode(frequencies)
    wrtie_file(characters,file)



if __name__ == '__main__':
    while (True):
        file = readCommand(str(sys.argv[1]))
        receiver(file)
