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

LOW_FREQ = 2000

HIGH_FREQ = 7000
#character to frequency translation dictionary
hex_to_freq={}
for x in range(0,10):
	hex_to_freq[str(x)] =875 *x + 1000
hex_to_freq['A'] = 875*10 + 1000 
hex_to_freq['B'] = 875*11 + 1000 
hex_to_freq['C'] = 875*12 + 1000 
hex_to_freq['D'] = 875*13 + 1000 
hex_to_freq['E'] = 875*14 + 1000 
hex_to_freq['F'] = 875*15 + 1000 

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
		ascii_key = ord(x)
		print(x)
		binary_ascii ="0x%0.2X" % ascii_key
		frequencies.append(hex_to_freq[binary_ascii[2]])
		frequencies.append(hex_to_freq[binary_ascii[3]])
	print(frequencies)
	return frequencies

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequencies, length=0.04, rate=44100):
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


