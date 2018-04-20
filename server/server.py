from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
from pprint import pprint
from MazeJsonManager import *
from ImageProcessor import *
import base64


"""
Maze Solver Request Handler (for server)
"""
class MazeSolverRequestHandler(BaseHTTPRequestHandler):

	def _set_headers_for_simple_acknowledgement(self):
		self.send_response(200)
		self.end_headers()

	#simple ping to server
	def _set_hello_header(self):
		self.send_response(200)
		self.send_header("Content-type", "text")
		self.end_headers()
		self.wfile.write("Hello!".encode())
	
	def _set_headers_for_send_image(self,image_name):
		image = open(image_name, 'rb')
		self.send_response(200)
		self.send_header("Content-type", "image/jpg")
		self.end_headers()
		
		#encode bytes for jpg
		img_bytes = base64.b64encode(image.read())
		image.close()
		data = open('dump.txt', 'wb')
		data.write(img_bytes)
		data.close()
		
		self.wfile.write(img_bytes)

	def _solve_maze(self):
		content_length = int(self.headers['Content-Length'])
		
		#decode bytes from jpg received from application
		image = base64.b64decode(self.rfile.read(content_length))

		with open("maze.jpg", 'wb') as ms:
			ms.write(image)

		image_solver = ImageProcessor.process_image("maze.jpg", 4)
		self._set_headers_for_send_image("solution.jpg")

	def do_GET(self):
		if "/solutions" in self.path:
			info = self.path[1:].split("/")
			maze_image = info[1]
			self._set_headers(maze_image)
		if "/hello" in self.path:
			self._set_hello_header()
			
	def do_POST(self):
		if "/solve" in self.path:
			self._solve_maze()
		
if __name__ == "__main__":
	server_class = HTTPServer
	httpd = server_class(("", 80), MazeSolverRequestHandler)
	httpd.serve_forever()
