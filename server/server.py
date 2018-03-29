from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

class MazeSolverRequestHandler(BaseHTTPRequestHandler):

	def _set_headers_for_simple_acknowledgement(self):
		self.send_response(200)
		self.end_headers()
	def _set_hello_header(self):
		self.send_response(200)
		self.send_header("Content-type", "text")
		self.end_headers()
		self.wfile.write("Hello!".encode())
	
	def _set_headers_for_send_image(self,image_name):
		image = open(image_name, 'rb')
		self.send_response(200)
		self.send_header("Content-type", "image/png")
		self.end_headers()
		self.wfile.write(image.read())

	def _solve_maze(self):
		content_length = int(self.headers['Content-Length'])
		image = self.rfile.read(content_length)
		with open("maze_solution.png", 'wb') as ms:
			#need a table to image dumper
			ms.write(image)
		self._set_headers_for_send_image("maze_solution.png")

	def do_GET(self):
		if "/solutions" in self.path:
			info = self.path[1:].split("/")
			maze_image = info[1]
			self._set_headers(maze_image)
		if "/hello" in self.path:
			print("GOT REQUEST")
			self._set_hello_header()
			

	def do_POST(self):
		if "/solve" in self.path:
			self._solve_maze()


if __name__ == "__main__":
	server_class = HTTPServer
	httpd = server_class(("localhost", 80), MazeSolverRequestHandler)
	httpd.serve_forever()
