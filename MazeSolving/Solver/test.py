from MazeJsonManager import *
from MazeBuilder import *
from pprint import pprint
from MazeSolver import *


MazeJsonManager.table_from_csv("tm.csv")
cells = MazeJsonManager.load_cell_table("table.json")
G = MazeBuilder.build_maze(cells)

path = MazeSolver.solve_maze(G)