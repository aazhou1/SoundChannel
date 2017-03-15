''''
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
import time

#character to frequency translation dictionary
hex_to_freq={}
for x in range(0,10):
	hex_to_freq[str(x)] =int(187.5 *x + 4000)

hex_to_freq['A'] = int(187.5*11 + 4000 )
hex_to_freq['B'] = int(187.5*12 + 4000 )
hex_to_freq['C'] = int(187.5*13 + 4000 )
hex_to_freq['D'] = int(187.5*14 + 4000 )
hex_to_freq['E'] = int(187.5*15 + 4000) 
hex_to_freq['F'] = int(187.5*16 + 4000 )

interm = int(187.5*10+4000)

#read text file data into a string
def read_file(file_name):
	to_transmit = open(file_name,"r")
	data = to_transmit.read()
	to_transmit.close()
	return data

#Translate string into sound frequency array
def encode(str):
	frequencies = []
	frequencies.append(9000)
	for x in str:
		ascii_key = ord(x)
		binary_ascii ="0x%0.2X" % ascii_key
		frequencies.append(hex_to_freq[binary_ascii[2]])
		frequencies.append(interm)
		frequencies.append(hex_to_freq[binary_ascii[3]])
		frequencies.append(interm)
	frequencies.append(9000)
	return frequencies

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequencies, length=0.042, rate=44100):
    chunks = []
    for frequency in frequencies:
        chunks.append(sine(frequency, length, rate))
        chunk = numpy.concatenate(chunks) * 0.25
    for t in range(5,-1,-1):
    	print t # Python v2 only
    	time.sleep(1.0)
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


