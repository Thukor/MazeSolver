class Node:
	def __init__(self, coordinate):
		self.coordinate = (*coordinate)
		self.neighbors = []

	def __hash__(self):
		return hash(self.coordinate)

	def __str__(self):
		return str(self.coordinate)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		return str(self) == str(other)


	def with_neighbor(self, node):
		self.neighbors.append(node)
		return self #Return self for potential object chaining
