from Node import *

class Edge:
	def __init__(self, node1, node2):
		self.edge = (node1,node2)
	def __hash__(self):
		return hash(self.edge)
	def __str__(self):
		return f"{self.edge[0]} -> {self.edge[1]}"
	def __repr__(self):
		return str(self)
	def __eq__(self, other):
		return self.edge == other.edge or (*reversed(self.edge)) == other.edge
		