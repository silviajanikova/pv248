# PV248 Python - exercise 02
# Author: Silvia Janikova 475938@muni.cz

import sys
from scorelib import load

if len(sys.argv) != 2:
	print('nespravny pocet argumentov')
	sys.exit(1)


for record in load(sys.argv[1]):
	record.format()

