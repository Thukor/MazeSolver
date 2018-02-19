from Node import *
from Edge import *
from pprint import pformat
from collections import defaultdict


class Graph:

	def __init__(self):
		self.adjacency_list = defaultdict(set)
		self.vertex_set = set()
		self.edge_set = set()

	def with_edge(self, edge_component1, edge_component2):
		node1 = Node(edge_component1) # create node for component 1
		node2 = Node(edge_component2) # create node for component 2
		edge = Edge(node1,node2)  #create edge for nodes
		self.vertex_set.add(node1)
		self.vertex_set.add(node2)
		self.edge_set.add(edge) #add edge to edge set
		self.adjacency_list[node1].add(node2) #add to adjacency list
		self.adjacency_list[node2].add(node1) #add to adjacency list
		return self #Return self for object chaining

	def with_node(self, vertex_value):
		node = Node(vertex_value)
		self.vertex_set.add(node)
		return self #Return self for object chaining

	def __str__(self):
		return pformat(self.adjacency_list)

	def __repr__(self):
		return str(self)

