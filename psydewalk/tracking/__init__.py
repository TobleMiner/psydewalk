from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread

tracked = {}

class TrackingRequestHandler(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		url = urlparse(self.path)
		query = parse_qs(url.query)
		if not 'entity' in query:
			self.wfile.write(b"<html><body>No id given</body></html>")
			return
		id = query['entity'][0]
		if not id in tracked:
			self.wfile.write(b"<html><body>Unknown id</body></html>")
			return
		entity = tracked[id]
		coord = entity.getLocation()
		self.wfile.write(bytes('{0};{1};{2}'.format(coord.lat, coord.lng, entity.getSpeed()), 'UTF-8'))

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		self._set_headers()
		self.wfile.write(b"<html><body><h1>POST!</h1></body></html>")

class TrackingServer():
	def __init__(self, port=8080, host='127.0.0.1'):
		self.port = port
		self.host = '127.0.0.1'

	def track(self, id, entity):
		if id in tracked:
			raise Exception('Id already tracked')
		tracked[id] = entity

	def untrack(self, id, entity):
		if id in tracked:
			tracked.pop(id, None)

	def run(self):
		server_address = (self.host, self.port)
		httpd = HTTPServer(server_address, TrackingRequestHandler)
		print('Starting tracking server...')
		httpd.serve_forever()

	def runInBackground(self):
		Thread(target=self.run, daemon=True).start()
