from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
from pprint import pprint
from MazeJsonManager import *
from ImageProcessor import *

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
		
		with open("maze.png", 'wb') as ms:
			ms.write(image)

		image_solver = ImageProcessor.process_image("maze.png", 4)
		self._set_headers_for_send_image("solution.png")

	def do_GET(self):
		if "/solutions" in self.path:
			info = self.path[1:].split("/")
			maze_image = info[1]
			self._set_headers(maze_image)
		if "/hello" in self.path:
			print("GOT A REQUEST")
			self._set_hello_header()
			

	def do_POST(self):
		if "/solve" in self.path:
			print("WE GOT AN IMAGE GUYS!!!!!")
			self._solve_maze()
		if "/demo" in self.path:
			content_length = int(self.headers['Content-Length'])
			image = self.rfile.read(content_length)
			table = MazeJsonManager.load_cell_table("table.json")
			pprint("GOT TABLE\n")
			pprint(table)
			self._set_headers_for_send_image("maze_output.png")			


if __name__ == "__main__":
	server_class = HTTPServer
	httpd = server_class(("", 80), MazeSolverRequestHandler)
	httpd.serve_forever()
