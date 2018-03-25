from networkx.algorithms.traversal import *
from networkx.algorithms.shortest_paths import *

def nx_shortest_path(G, start, end):
	return shortest_path(G,start,end)

def a_star(G, start, end, heuristic):
	return astar_path(G, start, end, heuristic)

def dijkstra_shortest_path(G, start, end):
	return dijsktra_path(G, start, end)


def manhattan_distance(c1,c2):
	return abs(c1.row - c2.row) + abs(c1.column - c2.column)

def euclidean_distance(c1,c2):
	return ((c1.row-c2.row)**2 + (c1.column-c2.column)**2)**.5

def chebyshev_distance(c1,c2):
	return max(abs(c1.row - c2.column), abs(c1.column - c2.column))
