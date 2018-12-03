# PV248 Python - exercise 09
# Author: Silvia Janikova 475938@muni.cz

# ./http-forward.py 9001 example.com

import sys
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlparse
from urllib.error import HTTPError, URLError

from socket import timeout


TIMEOUT = 1
CODE_OK = 200

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
	def json_validator(self, data):
		try:
			data_dict = json.loads(data)
			if 'type' not in data:
				data_dict['type'] = 'GET'

			if data_dict['type'] == 'POST' and 'content' not in data_dict:
				return False

			if 'url' not in data_dict:
				return False
			
			return True
		except ValueError as error:
			print("invalid json: %s" % error)
			return False


	# get code/headers/json
	def do_GET(self):
		resp_client = {}
		try:
			headers = dict(self.headers)
			headers['Accept-Encoding'] = 'identity'
			del headers["Host"]

			request = Request(url, 
				method='GET', 
				headers=headers)

			with urlopen(request, timeout=TIMEOUT) as resp:
				resp_client['code'] = resp.getcode()
				resp_client['headers'] = dict(resp.getheaders())
				content = resp.read().decode('utf-8')
				try:
					resp_client['json'] = json.loads(content)
				except:
					resp_client['content'] = content

				resp.close()
		except timeout:
			resp_client['code'] = 'timeout'

		self.send_response(CODE_OK)
		self.send_header('Connection', 'close')
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(resp_client), 'utf-8'))

		
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		encoded_data = post_data.decode('utf-8')
		resp_client = {}

		if self.json_validator(encoded_data):
			data_dict = json.loads(encoded_data)
			
			if 'type' not in data_dict:
				data_dict['type'] = 'GET'

			custom_timeout = 1
			if 'timeout' in data_dict:
				custom_timeout = int(data_dict['timeout'])

			request = Request(data_dict['url'], 
				method=data_dict['type'])

			if 'headers' in data_dict and type(data_dict['headers']) is dict:
				request.headers = data_dict['headers']
			
			if data_dict['type'] == 'POST':
				request.data = bytes(data_dict['content'], 'utf-8')

			try:
				with urlopen(request, timeout=custom_timeout) as resp:
					resp_client['code'] = resp.getcode()
					resp_client['headers'] = dict(resp.getheaders())
					content = resp.read().decode('utf-8')
					try:
						resp_client['json'] = json.loads(content)
					except:
						resp_client['content'] = content
			except HTTPError as error:
				resp_client['code'] = error.code
			except URLError as error:
				resp_client['code'] = 'invalid json'
			except timeout:
				resp_client['code'] = 'timeout'
			# except:
				# resp_client['code'] = 'invalid json'


		else:
			resp_client['code'] = 'invalid json'
		
		self.send_response(CODE_OK)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(resp_client), 'utf-8'))
		

def check_url(url):
	o = urlparse(url)
	if o.scheme == '':
		url = 'http://' + url
		url += ':80'
	return url


if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)

# parse arguments
port = int(sys.argv[1])
url = check_url(sys.argv[2])

httpd = HTTPServer(('localhost', port), CustomHTTPRequestHandler)
httpd.serve_forever()