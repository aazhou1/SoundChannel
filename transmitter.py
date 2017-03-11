'''
Andrew Zhou
Sheng Tan
UC Berkeley
EE 126 Spring 2017 Project

'''

from ToneGenerator import ToneGenerator

#character to frequency translation dictionary
char_to_freq={}



#read text file data into a string
def read_file(file_name):
	to_transmit = open(file_name,"r")
	data = to_transmit.read()
	to_transmit.close()
	return data

#Translate string into sound frequency array
def encode(str):

'''
ADD CODE
'''


#Main Function for transmitting data
def transmit(file_name):
	data = read_file(file_name)
	sounds = translate(data)
	generator = ToneGenerator()
	for frequency in sounds:

		#TODO: set step_duration, amplitude
		generator.play(frequency, step_duration, amplitude)


if __name__ == '__main__':
	file = readCommand(sys.argv[1])
	transmit(file)


