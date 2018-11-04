# PV248 Python - exercise 06
# Author: Silvia Janikova 475938@muni.cz

import sys
import wave, struct, numpy
from numpy import fft

# ./peaks.py audio.wav

if len(sys.argv) != 2:
	print('wrong number of arguments')
	sys.exit(1)

file_name = sys.argv[1]
wave_file = wave.open(file_name, 'r')

num_frames = wave_file.getnframes()
raw_data = wave_file.readframes(num_frames)

num_channels = wave_file.getnchannels()
sample_width = wave_file.getsampwidth()

total_samples = num_frames * num_channels

if sample_width == 1: 
	fmt = "%iB" % total_samples # read unsigned chars
elif sample_width == 2:
	fmt = "%ih" % total_samples # read signed 2 byte shorts

integer_data = struct.unpack(fmt, raw_data)

print(integer_data)

