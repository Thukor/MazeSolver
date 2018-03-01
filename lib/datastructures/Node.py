class Node:
	def __init__(self, coordinate):
		self.coordinate = (*coordinate)
		self.north = None
		self.south = None
		self.east = None
		self.west = None

	def __hash__(self):
		return hash(self.coordinate)

	def __str__(self):
		return str(self.coordinate)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		return str(self) == str(other)
