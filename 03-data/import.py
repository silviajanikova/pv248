# PV248 Python - exercise 03
# Author: Silvia Janikova 475938@muni.cz

import sys
import sqlite3
from scorelib import load

SQL_PERSON = "INSERT INTO person(born,died,name) VALUES(?,?,?)"
SQL_SCORE = "INSERT INTO score(name,genre,key,incipit,year) VALUES(?,?,?,?,?)"
SQL_SCORE_AUTHOR = "INSERT INTO score_author(score,composer) VALUES(?,?)"
SQL_VOICE = "INSERT INTO voice(number,score,name,range) VALUES(?,?,?,?)"
SQL_EDITION = "INSERT INTO edition(score,name) VALUES(?,?)"
SQL_PRINT = "INSERT INTO print(id,partiture,edition) VALUES(?,?,?)"
SQL_EDITION_AUTHOR = "INSERT INTO edition_author(edition,editor) VALUES(?,?)"


def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn


def create_tables(conn, sql_file):
	file = open(sql_file, 'r')
	file_content = file.read()
	file.close()

	sql_commands = file_content.split(';')
	for command in sql_commands:
		conn.execute(command)


def create_task(cur, sql, task):
	cur.execute(sql, task)
	return cur.lastrowid

def select(cur, table_name, attribute_name, value):
	cur.execute("SELECT * FROM {0} WHERE {1} = ?".format(table_name, attribute_name), (value,))
	return cur.fetchall()

# imports unique names of authors/editors to db
def import_person(cur, author):
	# check born/died info
	if author.born != None:
		cur.execute("SELECT born FROM person WHERE name = ? ", (author.name,))
		born = cur.fetchall()
		if born[0][0] == None:
			cur.execute("UPDATE person SET born = ? WHERE name = ? ",(author.born, author.name))

	if author.died != None:
		cur.execute("SELECT died FROM person WHERE name = ? ", (author.name,))
		died = cur.fetchall()
		if died[0][0] == None:
			cur.execute("UPDATE person SET died = ? WHERE name = ? ",(author.died, author.name))


def import_score(cur, composition):
	cur.execute("SELECT name FROM person WHERE name = ?", (author.name,))


def import_data(conn, obj):
	cur = conn.cursor()
	a = True

	unique_editions = list()
	unique_compositions = list()
	unique_persons = list()
	for record in obj:

		composition = record.edition.composition
		edition = record.edition

		for author in composition.authors + edition.authors:
			if author not in unique_persons:
				unique_persons.append(author)
				create_task(cur, SQL_PERSON, (author.born, author.died, author.name))
			else:
				import_person(cur, author)


		score_id = 0
		if composition not in unique_compositions:
			unique_compositions.append(composition)
			score_id = create_task(cur, SQL_SCORE, (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
			record.edition.composition.db_id = score_id

			for author in composition.authors:
				cur.execute("SELECT id FROM person WHERE name = ?", (author.name,))
				author_id = cur.fetchall()
				create_task(cur, SQL_SCORE_AUTHOR, (score_id, author_id[0][0]))

			for i, voice in enumerate(composition.voices):
				create_task(cur, SQL_VOICE, (i+1, score_id, voice.name, voice.range))

		else:
			for c in unique_compositions:
				if composition == c:
					score_id = c.db_id
					break

		if edition not in unique_editions:
			unique_editions.append(edition)
			edition_id = create_task(cur, SQL_EDITION, (score_id, edition.name))
			edition.db_id = edition_id

			for editor in edition.authors:
				cur.execute("SELECT id FROM person WHERE name = ?", (editor.name,))
				editor_id = cur.fetchall()
				create_task(cur, SQL_EDITION_AUTHOR,(edition_id, editor_id[0][0]))

		else:
			for e in unique_editions:
				if edition == e:
					edition_id = e.db_id		
					break

		create_task(cur, SQL_PRINT,(record.print_id, "Y" if record.partiture else "N", edition_id))

## ./import.py scorelib.txt scorelib.dat
sql_file_name = "scorelib.sql"

if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)    

# connect to database
conn = create_connection(sys.argv[2])
if conn != None:
	create_tables(conn, sql_file_name)
	import_data(conn, load(sys.argv[1]))
	conn.commit()