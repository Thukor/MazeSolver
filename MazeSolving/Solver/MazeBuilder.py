from networkx import nx
from Cell import *

class MazeBuilder:

	@staticmethod 
	def build_maze(cell_table):

		#Initialize maze as directed graph
		maze = nx.DiGraph()

		#flatten cell table by one level and map to Cell object
		cell_reference_table = {}

		#Add all possible cells to graph and update reference table
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

		#Helper method to recursively add edges to graph
		def rec_add_edges(row,column):

			#Origin base case or out of bounds base case
			if (row == 0 and column == 0) or row < 0 or column < 0:
				return

			#Extract cell of interest from table
			cell = cell_reference_table[(row,column)]

			#if no north wall exists, then a directed from
			#from the cell north of the current cell to the
			#current cell exists.
			if not cell.has_north_wall:
				north_cell = cell_reference_table[(row-1,column)]
				maze.add_edge(north_cell, cell)
				rec_add_edges(row-1, column)

			#if no west wall exists, then a directed from
			#from the cell west of the current cell to the
			#current cell exists.
			if not cell.has_west_wall:
				west_cell = cell_reference_table[(row,column-1)]
				maze.add_edge(west_cell, cell)
				rec_add_edges(row, column-1)

		#Add all edges to Maze recursively
		rec_add_edges(len(cell_table)-1, len(cell_table[0])-1)
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
		1: 5
	},
	1: {
		0: 6,
		1: 6
	},
	2: {
		0: 10,
		1: 8
	}
}


