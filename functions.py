"""
Miscellaneous functions.
"""

import struct

def die(message):
	from sys import exit
	print message
	exit()
	
def unpackBits(data):
	"""Get a list of booleans from any number of bytes.
	
	Returns bits in ascending size, bytes in order they were given."""
	bits = list()
	for char in data:
		for i in range(8):
			if (ord(char) & (1 << i)):
				bits.append(True)
			else:
				bits.append(False)
	return bits

def unpack16(data, bigEndian=False):
	"""Get an integer value from two bytes"""
	if bigEndian:
		return (ord(data[0]) * 256) + ord(data[1])
	else:
		return (ord(data[1]) * 256) + ord(data[0])

def sunpack16(data, bigEndian=False):
	"""Get a signed integer value from two bytes"""
	if bigEndian:
		return struct.unpack(">h", data)[0]
	else:
		return struct.unpack("<h", data)[0]

def unpack24(data, bigEndian=False):
	"""Get an integer value from three bytes"""
	if bigEndian:
		return (ord(data[0]) * 256 * 256) + (ord(data[1]) * 256) + ord(data[2])
	else:
		return (ord(data[2]) * 256 * 256) + (ord(data[1]) * 256) + ord(data[0])

def str2hex(str):
	"""Convert a string to a string of hex"""
	result = ''
	for c in str:
		result += hex(ord(c)) + ' '
	
	return result
	
def null_terminated_string(str):
	"""Returns the given string, up to the first null byte."""
	for i in range(len(str)):
		if str[i] == '\0':
			return str[0:i]
	
	# No nulls found, so return whole string
	return str
