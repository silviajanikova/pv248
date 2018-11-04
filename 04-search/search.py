# PV248 Python - exercise 04
# Author: Silvia Janikova 475938@muni.cz

import sys
import sqlite3
import json

# SQL_GET_PRINT = "SELECT p.id, p.partiture FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id LEFT JOIN score_author sa ON sa.score = s.id LEFT JOIN person per ON sa.composer = per.id WHERE per.name LIKE ?"

SQL_GET_PRINT = "SELECT p.id, p.partiture FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id LEFT JOIN score_author sa ON sa.score = s.id LEFT JOIN person per ON sa.composer = per.id WHERE per.name = ?"

SQL_GET_NAMES = "SELECT per.name FROM person per LEFT JOIN score_author sa  ON sa.composer = per.id WHERE per.name LIKE ? GROUP BY per.name"

SQL_GET_SCORE = "SELECT s.name, s.genre, s.key, s.year, s.incipit, e.name FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id WHERE p.id = ?"

SQL_GET_SCORE_ID = "SELECT s.id FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id WHERE p.id = ?"

SQL_GET_COMPOSERS = "SELECT per.name, per.born, per.died FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN score s on e.score = s.id LEFT JOIN score_author sa ON sa.score = s.id LEFT JOIN person per ON sa.composer = per.id WHERE p.id = ?"

SQL_GET_EDITORS = "SELECT per.name, per.born, per.died FROM print p LEFT JOIN edition e on p.edition = e.id LEFT JOIN edition_author ea ON ea.edition = e.id LEFT JOIN person per ON ea.editor = per.id WHERE p.id = ?"

SQL_GET_VOICES = "SELECT voice.number, voice.range, voice.name FROM voice WHERE voice.score = ?"



def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn


def clear_dict(d):
	for k, v in dict(d).items():
		if v is None:
			del d[k]
	return d


def get_authors(sql, print_id):
	cur.execute(sql, (print_id,))
	authors = cur.fetchall()
	authors_list = list()

	for a in authors:
		authors_dict = dict()
		authors_dict["name"] = a[0]
		authors_dict["born"] = a[1]
		authors_dict["died"] = a[2]
		authors_dict_c = clear_dict(authors_dict)
		if len(authors_dict_c) != 0:
			authors_list.append(authors_dict_c)

	return authors_list


def get_voices(print_id):
	cur.execute(SQL_GET_SCORE_ID, (print_id,))
	score_id = cur.fetchall()

	cur.execute(SQL_GET_VOICES, (score_id[0][0],))
	voices = cur.fetchall()
	# voices_list = list()
	voices_dict = dict()

	for v in voices:
		voice_dict = dict()
		voice_dict["name"] = v[2]
		voice_dict["range"] = v[1]
		voice_dict_c = clear_dict(voice_dict)

		if len(voice_dict_c) != 0:
			voices_dict[v[0]] = voice_dict_c

	return voices_dict


# ./search.py bach
if len(sys.argv) != 2:
	print("wrong number of arguments")
	sys.exit(1)  

# connect to database
db_name = "scorelib.dat"
conn = create_connection(db_name)
if conn != None:
	cur = conn.cursor()

	# get print id of selected composers
	search_name = '%' + sys.argv[1] + '%'

	# cur.execute(SQL_GET_PRINT, (search_name,))
	cur.execute(SQL_GET_NAMES, (search_name,))
	names = cur.fetchall()
	conn.commit()


name_list = list()
n_dict = dict()

for n in names:
	print_list = list()

	cur.execute(SQL_GET_PRINT, (n[0],))
	results = cur.fetchall()
	for r in results:
		cur.execute(SQL_GET_SCORE, (r[0],))
		data_se = cur.fetchall()
		conn.commit()

		r_dict = dict()
		r_dict["Print Number"] = r[0]
		r_dict["Composer"] = get_authors(SQL_GET_COMPOSERS, r[0])
		r_dict["Title"] = data_se[0][0]
		r_dict["Genre"] = data_se[0][1]
		r_dict["Key"] = data_se[0][2]
		r_dict["Composition Year"] = data_se[0][3]
		r_dict["Edition"] = data_se[0][5]
		r_dict["Editor"] = get_authors(SQL_GET_EDITORS,r[0])
		r_dict["Voices"] = get_voices(r[0])
		r_dict["Partiture"] = True if r[1] == "Y" else False
		r_dict["Incipit"] = data_se[0][4]

		r_dict_c = clear_dict(r_dict)
		print_list.append(r_dict_c)

	n_dict[n[0]] = print_list

print(json.dumps(n_dict,indent=4,ensure_ascii=False))