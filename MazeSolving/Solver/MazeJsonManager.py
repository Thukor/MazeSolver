import json
from collections import defaultdict
class MazeJsonManager:

	@staticmethod 
	def dump_cell_table(cell_table, filename):
		with open(filename, 'w') as jfp:
			json.dump(cell_table, jfp)

	@staticmethod
	def load_cell_table(filename):
		with open(filename, 'r') as jfp:
			return json.load(jfp)

	@staticmethod
	def dump_maze_and_solution_path(maze, solution, filename):

		total_table = {}

		cells = defaultdict(lambda: defaultdict(dict))

		for cell in maze.nodes():
			cells[int(cell.row)][int(cell.column)]["north"] = 1 if cell.has_north_wall else 0
			cells[int(cell.row)][int(cell.column)]["east"] = 1 if cell.has_east_wall else 0
			cells[int(cell.row)][int(cell.column)]["south"] = 1 if cell.has_south_wall else 0
			cells[int(cell.row)][int(cell.column)]["west"] = 1 if cell.has_west_wall else 0

		total_table["maze"] = cells 

		solution_path = []

		for cell in solution:
			solution_path.append((cell.row, cell.column))

		total_table["solution"] = solution_path

		MazeJsonManager.dump_cell_table(total_table, filename)
