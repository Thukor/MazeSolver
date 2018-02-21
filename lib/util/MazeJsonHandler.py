import json

class MazeJsonHandler:

	@staticmethod 
	def dump_cell_table(cell_table, filename):
		with open(filename, 'w') as jfp:
			json.dump(cell_table, jfp)

	@staticmethod
	def load_cell_table(filename):
		with open(filename, 'r') as jfp:
			return json.load(jfp)

