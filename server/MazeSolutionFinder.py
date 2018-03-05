from ..util.MazeBuilder import *
from ..util.MazeBuilderUtil import *
from ..util.PathFinding.pathfinding_algorithms import *
from ..util.PathFinding.a_star_heuristics import *
from ..util.MazeJsonHandler import *


def valid_border_openings(table):
	openings = []
	#Iterate over border of maze
	for i in range(len(table)):
		if not has_west_wall(table[i][0]):
			openings.append((i,0))
		if not has_east_wall(table[i][-1]):
			openings.append((i,len(table)-1))
		if not has_north_wall(table[0][i]):
			openings.append((0,i))
		if not has_south_wall(table[-1][i]):
			openings.append((len(table)-1, i))
	return tuple(openings) #should only have two elements

def get_solution_to_maze(table, strategy = nx_shortest_path):
	Maze = MazeBuilder.buld_maze(table)
	start,end = valid_border_openings(table)	
	return strategy(maze, start, end)

def load_table(filename):
	return MazeJsonHandler.load_cell_table(filename)