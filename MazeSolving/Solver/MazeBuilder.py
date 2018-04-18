from networkx import nx
from Cell import *

class MazeBuilder:

	@staticmethod 
	def build_maze(cell_table):

		#Initialize maze as directed graph
		maze = nx.Graph()

		#flatten cell table by one level and map to Cell object
		cell_reference_table = {}

		#Add all possible cells to graph and update reference table
		# print(len(cell_table[0]))
		for row in cell_table:
			for column in cell_table[row]:
				#create cell
				cell = Cell(row, column, cell_table[row][column])

				#Notiy cell of its possibility of being a start
				if row == 0 and not cell.has_north_wall:
					cell.is_possible_start = True
				if row == len(cell_table) - 1 and not cell.has_south_wall:
					cell.is_possible_start = True
				if column == 0 and not cell.has_west_wall:
					cell.is_possible_start = True
				if column == len(cell_table[0]) - 1 and not cell.has_east_wall:
					cell.is_possible_start = True

				#update reference table
				cell_reference_table[(row,column)] = cell

				#add cell to maze
				maze.add_node(cell)

		
		for row in range(len(cell_table)-1,-1,-1):
			for column in range(len(cell_table[0])-1,-1,-1):

				cell = cell_reference_table[(row, column)]

				if not cell.has_north_wall and row > 0:
					north_cell = cell_reference_table[(row-1,column)]
					maze.add_edge(north_cell, cell)

				if not cell.has_west_wall and column > 0:
					west_cell = cell_reference_table[(row,column-1)]
					maze.add_edge(west_cell, cell)

		return maze




#Test Square Maze

"""
  --
  ## |
| ##	
  --
"""
test_maze = {
	0: {
		0: 1,
		1: 13
	},
	1: {
		0: 2,
		1: 5
	},
	2: {
		0: 10,
		1: 5
	}
}


