from .MazeBuilderUtil import *

class MazeBuilder:
	@staticmethod
	def build_maze(table):
		x_bound = len(table)
		y_bound = len(table[0])
		node_dict = {(i,j-1): Node((i,j-1)) for (i,j) in enumerate(range(x_bound))}
		def build_maze_helper(i,j):
			if i >= x_bound or i < 0:
				return None
			if j >= y_bound or y < 0:
				return None
			node = node_dict[(i,j)]
			if not has_north_wall(table[i][j]):
				node.north = build_maze_helper(i,j+1)
			if not has_south_wall(table[i][j]):
				node.south = build_maze_helper(i,j-1)
			if not has_east_wall(table[i][j]):
				node.east = build_maze_helper(i+1,j)
			if not has_west_wall(table[i][j]):
				node.west = build_maze_helper(i-1,j)
			return node
		return build_maze_helper(0,0)