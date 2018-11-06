# PV248 Python - exercise 06
# Author: Silvia Janikova 475938@muni.cz

import sys
import wave, struct, numpy
from numpy import fft

# ./peaks.py audio.wav

if len(sys.argv) != 2:
	print('wrong number of arguments')
	sys.exit(1)

# open file
file_name = sys.argv[1]
wave_file = wave.open(file_name, 'r')

num_channels = wave_file.getnchannels()
num_frames = wave_file.getnframes()
frame_rate = wave_file.getframerate()

# length of analyzed window, 1 second
window = frame_rate
window_samples = frame_rate * num_channels
num_window = (num_frames * num_channels) // window_samples

low = None
high = None

for i in range(num_window):
	data = wave_file.readframes(window)
	
	data_int = struct.unpack("%ih" % window * num_channels, data)

	# stereo
	if(num_channels == 2):
		channel_1 = (data_int[0::num_channels])
		channel_2 = (data_int[1::num_channels])
		data_int = numpy.mean(numpy.array([channel_1, channel_2]), axis=0)

	amplitudes_list = numpy.fft.rfft(numpy.array(data_int))
	amplitudes_abs_list = numpy.abs(amplitudes_list)
	amplitudes_avg = numpy.mean(amplitudes_abs_list)

	for f, amp in enumerate(amplitudes_abs_list):
		if amp >= (20 * amplitudes_avg):
			if low == None or f < low:
				low = f
			if high == None or f > high:
				high = f


if low == None and high == None:
	print('no peaks')
else:
	print("low = {0}, high = {1}".format(low, high))


# close file
wave_file.close()



