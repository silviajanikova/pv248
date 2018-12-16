# PV248 Python - exercise 09
# Author: Silvia Janikova 475938@muni.cz

# ./ttt.py port

import sys
import json
import http.server
import socketserver
from urllib.parse import parse_qs
import time 

CODE_OK = 200
CODE_ERROR = 400


def check_int(value):
	try:
		num = int(value)
	except ValueError:
		return False
	return True


class TicTacToe(object):
	def __init__(self, game_id):
		self.game_id = game_id
		self.next = 1
		self.board = [[0,0,0],[0,0,0],[0,0,0]]


	def do_step(self, player, x, y):
		if self.is_end(): 
			return False, 'game already ended'

		if player != int(self.next):
			return False, 'wrong player'
	
		if self.board[y][x] != 0:
			return False, 'field already taken'

		self.board[y][x] = player
		self.next = (player % 2) + 1 

		return True, 'ok'


	def is_winner(self, player):
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == player or \
			self.board[2][0] == self.board[1][1] == self.board[0][2] == player:
			return True

		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] == player or \
				self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
				return True
		return False


	def is_draw(self):
		draw = True
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0:
					draw = False
		return draw


	def is_end(self):
		if self.is_winner(1) or self.is_winner(2) or self.is_draw():
			return True
		else:
			return False



class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	games = []

	def start_game(self):
		new_game = TicTacToe(len(self.games))
		self.games.append(new_game)

		return {'id': new_game.game_id}


	def get_status(self, game_id):
		if check_int(game_id) and any(g.game_id == int(game_id) for g in self.games):
			game = self.get_game_by_id(int(game_id))
			if game.is_end():
				if game.is_winner(1):
					self.send_reponse(CODE_OK, {'winner': 1})
				elif game.is_winner(2):
					self.send_reponse(CODE_OK, {'winner': 2})
				elif game.is_draw():
					self.send_reponse(CODE_OK, {'winner': 0})
			else:
				self.send_reponse(CODE_OK, {'board': game.board, 'next': game.next})

		else:
			self.send_reponse(CODE_ERROR, 'selected game does not exist')

	def get_game_by_id(self, game_id):
		for game in self.games:
			if game.game_id == game_id:
				return game
		
		return None


	def play(self, game_id, player, x, y):
		if check_int(game_id) and not any(g.game_id == int(game_id) for g in self.games):
			self.send_reponse(CODE_ERROR, 'selected game does not exist')	
		elif check_int(player) and int(player) != 1 and int(player) != 2:
			self.send_reponse(CODE_ERROR, 'selected player does not exist')
		elif not check_int(x) or not check_int(y):
			self.send_reponse(CODE_ERROR, 'selected coordinates does not exist')
		elif (int(x) < 0 or int(x) > 2) or (int(y) < 0 or int(y) > 2):
			self.send_reponse(CODE_OK, {'status':'bad', 'message':'coordinates out of range'})
		else:
			game = self.get_game_by_id(int(game_id))

			status, msg = game.do_step(int(player), int(x), int(y))
			if status:
				self.send_reponse(CODE_OK, {'status':'ok'})
			else:
				self.send_reponse(CODE_OK, {'status':'bad', 'message': msg})



	def send_reponse(self, code, content):
		self.send_response(code)
		self.send_header('Connection', 'close')

		if code == CODE_ERROR:
			self.end_headers()
			self.wfile.write(bytes(content, 'utf-8'))

		elif code == CODE_OK:
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(bytes(json.dumps(content), 'utf-8'))


	def parse_params(self):
		# request with parameters
		if '?' in self.path:
			url = self.path.split('?')
			parsed_params = parse_qs(url[1])

			# starting game
			if url[0] == '/start':
				if (len(parsed_params) == 1) and ('name' in parsed_params):
					self.send_reponse(CODE_OK, self.start_game())
				else:
					self.send_reponse(CODE_ERROR, 'unknow parameters')
			# status
			elif url[0] == '/status':
				if (len(parsed_params) == 1) and ('game' in parsed_params):
					self.get_status(parsed_params['game'][0])
				else:
					self.send_reponse(CODE_ERROR, 'unknow parameters, game is required')

			# play
			elif url[0] == '/play':
				if (len(parsed_params) == 4) and ('game' in parsed_params) and ('player' in parsed_params) and ('x' in parsed_params) and ('y' in parsed_params):
					self.play(parsed_params['game'][0], parsed_params['player'][0], parsed_params['x'][0], parsed_params['y'][0])
				else:
					self.send_reponse(CODE_ERROR, 'unknow parameters')
			else:
				self.send_reponse(CODE_ERROR, 'unknow parameters')

		# request without parameters
		elif self.path == '/start':
			self.send_reponse(CODE_OK, self.start_game())
		else:
			self.send_reponse(CODE_ERROR, 'unknow parameters')
	
	# get 
	def do_GET(self):
		self.parse_params()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	pass


if len(sys.argv) != 2:
	print('wrong number of arguments')
	sys.exit(1)

# parse arguments
if check_int(sys.argv[1]):
	port = int(sys.argv[1])
else:
	print('expected port number')
	sys.exit(1)

httpd = ThreadedHTTPServer(('localhost', port), CustomHTTPRequestHandler)
httpd.serve_forever()