'''
Andrew Zhou
Sheng Tan
UC Berkeley
EE 126 Spring 2017 Project

Borrowed tone generation from:

http://milkandtang.com/blog/2013/02/16/making-noise-in-python/

Educational Use only--School Project
'''
import sys
import pyaudio
import numpy
import math

#character to frequency translation dictionary
char_to_freq={}
for x in range(256):
	char_to_freq[x] = x*60

#read text file data into a string
def read_file(file_name):
	to_transmit = open(file_name,"r")
	data = to_transmit.read()
	to_transmit.close()
	return data

#Translate string into sound frequency array
def encode(str):
	frequencies = []
	for x in str:
		frequencies.append(char_to_freq[ord(x)])
	return frequencies

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequencies, length=0.025, rate=44100):
    chunks = []
    for frequency in frequencies:
        chunks.append(sine(frequency, length, rate))

        chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())


#Main Function for transmitting data
def transmit(file_name):
	data = read_file(file_name)
	sounds = encode(data)
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
	play_tone(stream,sounds)


if __name__ == '__main__':
	file = str(sys.argv[1])
	transmit(file)


