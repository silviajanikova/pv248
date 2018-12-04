# PV248 Python - exercise 10
# Author: Silvia Janikova 475938@muni.cz

import sys
import json
import os.path
import urllib
import http.server
import socketserver

CODE_OK = 200

# class factory
def handler(dir_path):
	class CGIHandler(http.server.CGIHTTPRequestHandler):
		def do_GET(self):
			self.handle_cgi()
			
		def do_POST(self):
			self.handle_cgi()

		def handle_cgi(self):
			parsed_url = urllib.parse.urlparse(self.path[1:])
			request_path = parsed_url.path
			query_arguments = parsed_url.query
			result_path = os.path.join(dir_path, request_path)
			relative_path = os.path.relpath(result_path, os.getcwd())
			result = bytes('', 'utf-8')

			if os.path.isfile(result_path):
				if result_path.endswith('.cgi'):
					os.environ['QUERY_STRING'] = query_arguments
					os.environ['AUTH_TYPE'] = ''
					self.cgi_info = '/', relative_path
					self.run_cgi()

					return
				else:
					with open(result_path, 'rb') as requested_file:
						result = requested_file.read()

					self.send_response(CODE_OK)
					self.send_header('Content-Length', len(result))


			elif os.path.isdir(result_path):
				self.send_response(403)
			else:
				self.send_response(404)
				
			self.send_header('Connection', 'close')
			self.end_headers()
			self.wfile.write(result)


	h = CGIHandler
	h.cgi_directories = [dir_path]

	return h


# ./serve.py 9001 dir
if len(sys.argv) != 3:
	print('wrong number of arguments')
	sys.exit(1)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
	"""Handle requests in a separate thread."""

# parse arguments
port = int(sys.argv[1])
dir_path = sys.argv[2]
dir_path = os.path.abspath(dir_path)

if not os.path.isdir(dir_path):
	print('directory doesnt exist')
	sys.exit(2)

httpd = ThreadedHTTPServer(('localhost', port), handler(dir_path))
httpd.serve_forever()
