from MazeJsonManager import *
from MazeBuilder import *
from pprint import pprint
from MazeSolver import *
import networkx as nx
import matplotlib.pyplot as plt

MazeJsonManager.table_from_csv("tm.csv")
cells = MazeJsonManager.load_cell_table("table.json")
G = MazeBuilder.build_maze(cells)

start_end = []
for node in G:
	if node.is_possible_start:
		start_end.append(node)

path = MazeSolver.solve_maze(G)



other_nodes = set(G.nodes()) - set(start_end)

pos = nx.spring_layout(G)
nx.draw_networkx_edges(G,pos, edge_color='black')
nx.draw_networkx_nodes(G, pos, [n for n in path[1:-1]],node_color='green')
nx.draw_networkx_nodes(G, pos, [path[0], path[-1]],node_color='purple', node_size=500)
nx.draw_networkx_nodes(G, pos, set(G.nodes()) - set(path), node_color='blue', node_size=150)

plt.savefig("maze_output.png",format="PNG")
plt.show()


