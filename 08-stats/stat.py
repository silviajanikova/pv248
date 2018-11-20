# PV248 Python - exercise 08
# Author: Silvia Janikova 475938@muni.cz

# ./stat.py file.txt <mode>
#  mode = dates, deadlines, exercises

import sys, csv
import pandas, json
import numpy as np

def get_stats(data):
	values = {}
	values["mean"] = data.mean().item()
	values["median"] = data.median().item()
	values["first"] = np.percentile(data, 25).item()
	values["last"] = np.percentile(data, 75).item()
	values["passed"] = data[data > 0].count().item()

	return values


if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)

# parse arguments
file_name = sys.argv[1]
mode = sys.argv[2]

header = pandas.read_csv(file_name, nrows=0)
data = pandas.read_csv(file_name)

result = {}
dates = {}
exercises = {}

for col in header:
	col_splitted = col.split("/")

	if col != "student":
		if mode == "deadlines":
			result[col] = get_stats(data[col])
		elif mode == "dates":
			if col_splitted[0] in dates:
				dates[col_splitted[0]] = dates[col_splitted[0]].append(data[col])
			else:
				dates[col_splitted[0]] = data[col]

		elif mode == "exercises":
			if col_splitted[1] in exercises:
				exercises[col_splitted[1]].append(col)
			else:
				exercises[col_splitted[1]] = [col]

if mode == "dates":		
	for date, value in dates.items():
		result[date] = get_stats(value)
elif mode == "exercises":
	for exercise, value in exercises.items():		
		data[exercise] = data[value[0]] + data[value[1]]
		result[exercise] = get_stats(data[exercise])

print(json.dumps(result, indent=2))
