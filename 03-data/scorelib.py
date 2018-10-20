# PV248 Python - exercise 02
# Author: Silvia Janikova 475938@muni.cz

import sys
import re

# classes for print, edition, composition, voice, person
class Composition(object):
	def __init__(self, name = None, incipit = None, key = None, genre = None, year = None, voices = None, authors = None):
		self.db_id = 0
		self.name = name
		self.incipit = incipit
		self.key = key
		self.genre = genre
		self.year = year
		if voices == None:
			self.voices = list()
		else:
			self.voices = voices

		if authors == None:
			self.authors = list()
		else:
			self.authors = authors

		self._dict = None

	def get_dict(self):
		if self._dict == None:
			self._dict = { k: self.__dict__[k] for k in self.__dict__ if k != "db_id" or k != "_dict" }

		return self._dict

	def __eq__(self, other):

		return self.get_dict() == other.get_dict()


class Edition(object):
	def __init__(self, composition = None, authors = None, name = None):
		self.db_id = 0
		
		if composition == None:
			self.composition = Composition()
		else:
			self.composition = composition

		if authors == None:
			self.authors = list()
		else:
			self.authors = authors

		self.name = name
		
		self._dict = None

	def get_dict(self):
		if self._dict == None:
			self._dict = { k: self.__dict__[k] for k in self.__dict__ if k != "db_id" or k != "_dict" }

		return self._dict

	def __eq__(self, other):
		return self.get_dict() == other.get_dict()


class Print(object):
	def __init__(self, edition = None, print_id = 0, partiture = False):
		self.print_id = print_id
		self.partiture = partiture

		if edition == None:
			self.edition = Edition()
		else:
			self.edition = edition

	def format(self):
		print("Print Number: " + str(self.print_id))
		print("Composer: " + print_authors(self.edition.composition.authors, ";"))
		if self.composition().name:
			print("Title: " + self.composition().name)	

		if self.composition().genre:
			print("Genre: " + self.composition().genre)
	
		if self.composition().key:
			print("Key: " + self.composition().key)

		if self.composition().year:
			print("Composition Year: " + str(self.composition().year))

		if self.edition.name:
			print("Edition: " + self.edition.name)

		print("Editor: " + print_authors(self.edition.authors, ","))
		
		for i,v in enumerate(self.composition().voices):
			print("Voice " + str(i + 1) + ": " + print_voice(v))

		if self.partiture:
			print("Partiture: yes")
		else:
			print("Partiture: no")
		if self.composition().incipit:
			print("Incipit: " + self.composition().incipit)
		
		print()

	def composition(self):
		return self.edition.composition

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Voice(object):
	def __init__(self, name = None, range = None):
		self.name = name
		self.range = range

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


class Person(object):
	def __init__(self, name = "", born = None, died = None):
		self.name = name
		self.born = born
		self.died = died

	def __str__(self):
		return self.name

	def __eq__(self, other):
		return self.name == other.name


# vrati list objektov person
def parse_composer(data):
	# rozdeli na group pre meno a group pre zatvorky
	r_composer = re.compile(r"([^\(]*)\s*(\(.*\))?")
	r_year = re.compile(r"\(([0-9]*)--?([0-9]*)\)")
	composers = data.split(";")
	born = None
	died = None
	objs = list()

	for c in composers:
		composer_group = r_composer.match(c)
		if composer_group.group(2) != None:
			year_group = r_year.match(composer_group.group(2))
			if year_group != None:
				if try_parse_int(year_group.group(1)):
					born = int(year_group.group(1))
				if try_parse_int(year_group.group(2)):
					died = int(year_group.group(2))

		objs.append(Person(composer_group.group(1).strip(), born, died))
	return objs

def parse_editors(data):
	editors = list()
	if data.count(",") > 1:
		names = data.split(",")
		for i,n in enumerate(names):
			if i % 2 == 0:
				name = n.strip() + ", " + names[i+1].strip()
				editors.append(Person(name))
	else:
		editors.append(Person(data))

	return editors


def print_voice(voice):
	v = ""

	if voice.range != None:
		v += voice.range
		if voice.name != None:
			v += ", "
	
	if voice.name != None:
		v += voice.name

	return v

def parse_voice(line):
	voice = Voice()
	
	if line == None:
		return voice

	r_n = re.split(r",|;", line, 1)
	if len(r_n) == 1:
		if "--" in r_n[0]:
			voice.range = r_n[0].strip()
		else:
			voice.name = r_n[0].strip()
	else:
		if "--" in r_n[0]:
			voice.range = r_n[0].strip()
			voice.name = r_n[1].strip()
		else:
			voice.name = (r_n[0]+", "+r_n[1].strip()).strip()

	return voice


def print_authors(list_obj, sep):
	composers_content = ""
	for i,c in enumerate(list_obj):
		composers_content += c.name
		if c.born == None:
			born = ""
		else:
			born = str(c.born)

		if c.died == None:
			died = ""
		else:
			died = str(c.died)

		if born != "" or died != "":
			composers_content += " (" + born + "--" + died + ")"
		if i != len(list_obj)-1:
			composers_content += sep+" "

	return composers_content


def try_parse_int(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False


def parse_line(line):
	parsed = line.split(":",1)[1].strip()
	if parsed == "":
		return None
	return parsed


def parse_stanza(stanza):

	record = Print()
	record.edition = Edition()
	record.edition.composition = Composition()
		
	for line in stanza.splitlines():
		
		if not line:
			continue

		parsed = parse_line(line)

		if line.startswith("Print Number:"):
			record.print_id = int(parsed)

		if line.startswith("Composer:"):
			if parsed != None:
				record.edition.composition.authors = parse_composer(parsed)

		if line.startswith("Title:"):
			record.edition.composition.name = parsed

		if line.startswith("Genre:"):
			record.edition.composition.genre = parsed

		if line.startswith("Key:"):
			record.edition.composition.key = parsed

		if line.startswith("Composition Year:"):
			if parsed != None and try_parse_int(parsed):
				record.edition.composition.year = int(parsed)

		if line.startswith("Edition:"):
			record.edition.name = parsed

		if line.startswith("Editor:"):
			if parsed:
				record.edition.authors = parse_editors(parsed)
		
		if line.startswith("Voice"):
			record.edition.composition.voices.append(parse_voice(parsed))

		if line.startswith("Partiture:"):
			if parsed != None and parsed.startswith("yes"):
				record.partiture = True

		if line.startswith("Incipit:"):
			record.edition.composition.incipit = parsed

	return record

def load(filename):

	with open(filename, 'r') as f:
		stanza = ""
		printed_scores = list()

		line = f.readline()
		while line:
			if line == "\n" and stanza != "":
				printed_scores.append(parse_stanza(stanza))

				stanza = ""
				line = f.readline()
				continue

			stanza += line

			line = f.readline()
		
		if stanza != "":
			printed_scores.append(parse_stanza(stanza))

	return printed_scores