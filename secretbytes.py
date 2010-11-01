#!/usr/bin/env python

import glob
from functions import *

files = glob.glob('./worlds/*.dlw')

for file in files:
	f = open(file)
	f.seek(73)
	print file, str2hex(f.read(4))
