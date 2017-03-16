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
	hex_to_freq[str(x)] =int(400 *x + 1000)

hex_to_freq['A'] = int(400*12 + 1000 )
hex_to_freq['B'] = int(400*13 + 1000 )
hex_to_freq['C'] = int(400*14 + 1000 )
hex_to_freq['D'] = int(400*15 + 1000 )
hex_to_freq['E'] = int(400*16 + 1000) 
hex_to_freq['F'] = int(400*17 + 1000 )

interm = int(400*10.5+1000)

#read text file data into a string
def read_file(file_name):
	to_transmit = open(file_name,"r")
	data = to_transmit.read()
	to_transmit.close()
	return data

#Translate string into sound frequency array
def encode(str):
	frequencies = []
	ff = []
	frequencies.append(9000)
	for x in str:
		ascii_key = ord(x)
		binary_ascii ="0x%0.2X" % ascii_key
		frequencies.append(hex_to_freq[binary_ascii[2]])
		ff.append(hex_to_freq[binary_ascii[2]])
		frequencies.append(interm)
		frequencies.append(hex_to_freq[binary_ascii[3]])
		ff.append(hex_to_freq[binary_ascii[3]])
		frequencies.append(interm)
	frequencies.append(9000)

	return frequencies

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequencies, length=0.02, rate=44100):
	print("recommended record time is %f", length*len(frequencies))
	for t in range(5,-1,-1):
		print(t)
		time.sleep(1.0)
	for frequency in frequencies:
		if (frequency == 9000):
			chunks= [sine(frequency, 0.01, rate)]
		else:
			chunks = [sine(frequency, length, rate)]
		chunk = numpy.concatenate(chunks) * 0.25
		stream.write(chunk.astype(numpy.float32).tostring())
	print(frequencies)
    


#Main Function for transmitting data
def transmit(file_name):
	data = read_file(file_name)
	sounds = encode(data)
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
	play_tone(stream,sounds)


if __name__ == '__main__':
	file = str(sys.argv[1])
	now = time.time()
	transmit(file)
	future = time.time()
	print(future-now-5)



