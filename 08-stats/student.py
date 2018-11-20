# PV248 Python - exercise 08
# Author: Silvia Janikova 475938@muni.cz

# ./student.py file.csv <id>
#  <id> = id, average

import sys, csv
import pandas, json
import numpy as np
from datetime import datetime
from datetime import timedelta
from scipy import stats


def get_stats(student, prediction):
	values = {}
	values["mean"] = student.mean(axis=1).item()
	values["median"] = student.median(axis=1).item()
	values["passed"] = student[student > 0].count(axis=1).item()
	values["total"] = student.sum(axis=1).item()
	values["regression slope"] = prediction[0]
	values["date 16"] = prediction[1]
	values["date 20"] = prediction[2]
	return values


def get_prediciton(student, header, data):
	dates = {}
	points = 0
	for col in header:
		col_splitted = col.split("/")

		if col != "student":
			# points += data.loc[data["student"] == student, [col]].iat[0,0]
			
			if student == "average":
				points += (data.loc[["average"], [col]]).iat[0,0]
			else:
				points += (data.loc[data["student"] == student, [col]]).iat[0,0]

			dates[col_splitted[0]] = points
	
	if points == 0:
		return 0, 'inf', 'inf'
	
	semester_begin = datetime.strptime("2018-09-17", "%Y-%m-%d")

	points = list(dates.items())


	points = sorted([(v[1], (datetime.strptime(v[0], "%Y-%m-%d") - semester_begin).days) for v in points], key=lambda x: x[1])

	x = [v[0] for v in points]
	y = [v[1] for v in points]

	result = stats.linregress(x,y)
	slope = result[0]

	# y = a * x + 0
	y16 = slope * 16
	y20 = slope * 20

	date16 = semester_begin + timedelta(days=y16)
	date20 = semester_begin + timedelta(days=y20)

	return slope, date16.strftime("%Y-%m-%d"), date20.strftime("%Y-%m-%d")



if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)


# parse arguments
file_name = sys.argv[1]
student = int(sys.argv[2]) if sys.argv[2] != "average" else "average"

header = pandas.read_csv(file_name, nrows=0)
data = pandas.read_csv(file_name)


if student != "average" and student not in data["student"].tolist():
	print('wrong student number')
	sys.exit(1)


exercises = {}
# dict of exercises
for col in header:
	col_splitted = col.split("/")

	if col != "student":
		if col_splitted[1] in exercises:
			exercises[col_splitted[1]].append(col)
		else:
			exercises[col_splitted[1]] = [col]


if student == "average":
	data.loc["average"] = data.mean()

# exercises sum to dataframe
exercise_list = []
for exercise, value in exercises.items():
	data[exercise] = data[value[0]] + data[value[1]]
	exercise_list.append(exercise)

# points = list(get_points(student, header, data).items())
prediction = get_prediciton(student, header, data)

# find student, print stats
if student == "average":
	student_row = (data.loc[["average"], exercise_list])
else:
	student_row = (data.loc[data["student"] == student, exercise_list])

print(json.dumps(get_stats(student_row, prediction), indent=2))

		