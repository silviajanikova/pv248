# PV248 Python - exercise 04
# Author: Silvia Janikova 475938@muni.cz

import sys
import sqlite3
import json

SQL_PRINT = "SELECT per.name, per.born, per.died FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id LEFT JOIN score_author sa ON sa.score = s.id LEFT JOIN person per ON sa.composer = per.id WHERE p.id = ?"

def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn


def clear_dict(d):
	for k, v in dict(d).items():
		if v is None:
			del d[k]
	return d

# ./getprint.py 645
if len(sys.argv) != 2:
	print("wrong number of arguments")
	sys.exit(1)  

# connect to database
db_name = "scorelib.dat"
conn = create_connection(db_name)
if conn != None:
	cur = conn.cursor()
	cur.execute(SQL_PRINT, (sys.argv[1],))
	composers = cur.fetchall()
	conn.commit()

	composer_list = list()

	for c in composers:
		composer_dict = dict()
		composer_dict["name"] = c[0]
		composer_dict["born"] = c[1]
		composer_dict["died"] = c[2]
		composer_dict_c = clear_dict(composer_dict)
		composer_list.append(composer_dict_c)

	# print(composer_dict)
	print(json.dumps(composer_list,indent=4,ensure_ascii=False))
