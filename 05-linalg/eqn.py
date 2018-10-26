# PV248 Python - exercise 05
# Author: Silvia Janikova 475938@muni.cz

import sys
import numpy.linalg
import numpy

# ./eqn.py input.txt

def get_const_list(data):
	const_list = list()

	for eq in data:
		const_list.append(eq["constant"])

	return const_list


def get_variables(data):
	keys = set()
	for eq in data:
		for k, v in eq.items():
			if k == 'constant':
				continue
			keys.add(k)

	keys = sorted(keys)

	return keys


def get_coef_matrix(data):
	keys = get_variables(data)
	eqs_list =list()

	for eq in data:
		eq_list = list()
		for key in keys:
			if key in eq:
				eq_list.append(eq[key])
			else:
				eq_list.append(0)
		eqs_list.append(eq_list)

	return eqs_list


def parse_line(line):
	sides = line.split('=')

	coefficient = ""
	line_dict = dict()
	coef_minus = False

	# parse left side
	for c in sides[0]:
		if c.isdigit():
			coefficient += c

		elif c.isalpha() and c.islower():
			if coefficient != "":
				if coef_minus:
					line_dict[c] = int(coefficient) * (-1)
					coef_minus = False
				else:
					line_dict[c] = int(coefficient)
				coefficient = ""

			else: 
				if coef_minus:
					line_dict[c] = -1
					coef_minus = False
				else:
					line_dict[c] = 1
		elif c == "-":
			coef_minus = True

		else:
			continue

	# right side
	line_dict["constant"] = int(sides[1])

	return(line_dict)
		



filename = sys.argv[1]

with open(filename, 'r') as f:
	line = f.readline()
	eq_list = list()

	while line:
		eq_list.append(parse_line(line))
		line = f.readline()
	f.close()

# create augmented matrix
augmented_matrix = list()
const_list = get_const_list(eq_list)
i = 0

for l in get_coef_matrix(eq_list):
	l.append(const_list[i])
	i += 1
	augmented_matrix.append(l)

# compute rank for coefficient matrix
A = numpy.matrix(get_coef_matrix(eq_list))
rank_coef = numpy.linalg.matrix_rank(A)

# compute rank for augmented matrix
B = numpy.matrix(augmented_matrix)
rank_aug = numpy.linalg.matrix_rank(B)

keys = get_variables(eq_list)

if rank_coef != rank_aug:
	print("no solution")

elif rank_coef == len(keys):
	M1 = numpy.array(get_coef_matrix(eq_list))
	M2 = numpy.array(get_const_list(eq_list))
	result = list(numpy.linalg.solve(M1, M2))
	keys = keys
	a = list(zip(keys, result))
	res_str = ["{0} = {1}".format(k, v) for k,v in a]
	res_str = ", ".join(res_str)

	res_str = "solution: " + res_str
	print(res_str)


elif len(keys) > rank_coef:
	dimension = len(keys) - rank_coef
	print("solution space dimension: " + str(dimension))





		