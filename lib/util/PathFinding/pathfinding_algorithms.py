
from networkx.algorithm.traversal import *
from networkx.algorithm.shortest_paths import *


def nx_shortest_path(G, start, end):
	return shortest_path(G,start,end)

def a_star(G, start, end, heuristic):
	return astar_path(G, start, end, heuristic)

def dijkstra_shortest_path(G, start, end):
	return dijsktra_path(G, start, end)

