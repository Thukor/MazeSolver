from .MazeBuilderUtil import *
import networkx as nx 

class MazeBuilder:
	@staticmethod
	def build_maze(table):
		x_bound = len(table)
		y_bound = len(table[0])
		Maze = nx.Graph()
		def build_maze_helper(i,j):
			if i >= x_bound or i < 0:
				return None
			if j >= y_bound or y < 0:
				return None
			Maze.add_node((i,j))
			if not has_north_wall(table[i][j]):
				north_node = build_maze_helper(i,j+1)
				if north_node is not None:
					Maze.add_edge((i,j), north_node)
			if not has_south_wall(table[i][j]):
				south_node = build_maze_helper(i,j-1)
				if south_node is not None:
					Maze.add_edge((i,j), south_node)
			if not has_east_wall(table[i][j]):
				east_node = build_maze_helper(i+1,j)
				if east_node is not None:
					Maze.add_edge((i,j), east_node)
			if not has_west_wall(table[i][j]):
				west_node = build_maze_helper(i-1,j)
				if west_node is not None:
					Maze.add_edge((i,j), west_node)
			return (i,j)
		build_maze_helper(0,0)
		return Maze