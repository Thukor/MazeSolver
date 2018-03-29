from PathFinder import *
from pathfinding_algorithms import *

class MazeSolver:
	@staticmethod
	def solve_maze(maze):
		pf = PathFinder(nx_shortest_path)
		start_end = sorted([node for node in maze.nodes() if node.is_possible_start])
		heuristic = manhattan_distance
		return pf.find_shortest_path(maze,*start_end)