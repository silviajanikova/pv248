# PV248 Python - exercise 01
# Author: Silvia Janikova 475938@muni.cz

import sys
import re
from collections import Counter

# regex definition
r_composer_name = re.compile(r"([^\(]*)(\(.*\))?")
r_year = re.compile(r".*([0-9]{4})(?!.*\d{4})")

# function for convert year to "xxth century" format
def year_to_century(year):
	return str((year // 100) + 1) + "th century"


# function for regex compile
def add_regex(key):
	text = ""
	if key == "composer":
		text = "Composer"
	elif key == "century":
		text = "Composition Year"

	result = re.compile(r"" + text + ":(.*)")

	return result

# function for printing result
def print_results(results):
	for k,v in Counter(result).items():
		print(k + ': ' + str(v))


if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)

if sys.argv[2] == 'composer':
	result = []
	r_key = add_regex(sys.argv[2]);

	f = open(sys.argv[1], 'r')
	for line in f:
		match = r_key.match(line)

		if match != None:
			for composer_item in match.group(1).split(';'):
				composer_item = r_composer_name.match(composer_item)
				if composer_item.group(1).strip() != "":
					result.append(composer_item.group(1).strip())
	print_results(result)

elif sys.argv[2] == 'century':
	result = []
	r_key = add_regex(sys.argv[2]);

	f = open(sys.argv[1], 'r')
	for line in f:
		match = r_key.match(line)

		if match != None:
			century_item = match.group(1).strip()
			if "th century" in century_item:
				result.append(century_item)
			elif century_item !=  "":
				year = r_year.match(century_item).group(1)
				result.append(year_to_century(int(year)))	
	print_results(result)

else:
	print('unknown argument')
	sys.exit(1)
