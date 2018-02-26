class PathFinder:

	def __init__(self, graph):
		self.graph = graph

	@staticmethod
	def find_path(self, strategy):
		return strategy(self.graph)