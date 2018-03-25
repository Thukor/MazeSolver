import networkx as nx 


class Maze:

	def __init__(self):
		self.graph = nx.DiGraph()

	def add_cell(self, cell):
		coordinate = (cell.row, cell.column)
		self.graph.add_node(coordinate)

	def add_edge(self, cell1, cell2):
		coordinate1 = (cell1.row, cell1.column)
		coordinate2 = (cell2.row, cell2.column)

		self.graph.add_edge(coordinate1, coordinate2)