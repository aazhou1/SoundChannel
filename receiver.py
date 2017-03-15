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

from __future__ import division
import pyaudio
import wave
import numpy as np
import sys


freq_to_hex={}
for x in range(0,10):
    freq_to_hex[int(400 *x + 1000)] =str(x)

freq_to_hex[int(400*12 + 1000)] = 'A'
freq_to_hex[int(400*13 + 1000)] =  'B'
freq_to_hex[int(400*14 + 1000)]  = 'C'
freq_to_hex[int(400*15 + 1000)]= 'D'
freq_to_hex[int(400*16 + 1000)] = 'E'
freq_to_hex[int(400*17 + 1000)]  = 'F'
interm = int(400*10.5+1000)



#Write character string to output file
def write_file(data, filename):
    text_file = open(filename,"w")
    text_file.write(data)
    text_file.close()

#Translate Sound Frequencies into Character Strings
def decode(sounds):

    i = 0 
    find = []
    start_string = 0
    last_read = 0 
    characters =""
    while i < len(sounds)-1:
        #waiting for start of text signal from transmitter

        if (abs(9000 - sounds[i]) <= 50) and start_string == 0:

            start_string = 1
            #iterate until start signal is done
            while  (abs(9000 - sounds[i+1]) <= 50):
                i+=1
            i+=1
         #end for start of text signal from transmitter
        elif (abs(9000 - sounds[i]) <= 50) and start_string == 1:
            break

        elif (abs(interm - sounds[i]) <= 50) and start_string == 1:
            while ((abs(interm - sounds[i+1]) <= 50) or (abs(interm - sounds[i+2]) <= 50)):
                i+=1
            i+=1
        elif start_string == 1:
            print("hello %f",sounds[i])
            found = 0
            if (abs(sounds[i+1] - sounds[i]) <= 200) and (abs(sounds[i+2] - sounds[i]) <= 200):
                for x in range(int(sounds[i]), int(sounds[i])+200):
                    if x in freq_to_hex.keys():
                        print(x)
                        find.append(x)
                        characters+=freq_to_hex[x]
                        print(characters)
                        found = 1
                        break
            if found == 1 and i <len(sounds):
                while i < len(sounds)-1 and (abs(interm - sounds[i+1]) > 30) :
                    print("lebron %f", sounds[i])
                    i+=1
            i+=1
        else:
            i+=1
    output = ""
    i = 0 
    while i < len(characters):
        output += str(chr(int(characters[i:i+2],16)))
        i+=2
    print(find)
    return output



def receiver(file,time):
    #3-4 readings per bit

    CHUNK = 100
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = time
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
    print(len(frames))
    stream.close()
    p.terminate()

    i = 0
    frequencies =[]
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
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/CHUNK
            frequencies.append(thefreq)
            print("freq is %f", thefreq)

        else:
            thefreq = which*RATE/CHUNK
            frequencies.append(thefreq)
            print("freq is %f", thefreq)
        # read some more data
        i+=1
    characters = decode(frequencies)
    write_file(characters,file)



if __name__ == '__main__':
    
    file = str(sys.argv[1])
    time = int(sys.argv[2])
    receiver(file,time)
    to_transmit = open("test.txt","r")
    standard = to_transmit.read()
    to_transmit.close()
    transmitted = open("output.txt","r")
    data = transmitted.read()
    transmitted.close()
    i = 0 
    correct = 0
    while i < len(standard) and i<len(data):
        if standard[i] == data[i]:
            correct+=1
        i+=1
    print("Accuracy rate is %f", correct/i)

