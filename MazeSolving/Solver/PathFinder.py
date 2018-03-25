class PathFinder:

	#Instantiate for Strategy Pattern:  Context -> Path Finding
	def __init__(self, strategy):
		self.strategy = strategy
	
	def find_shortest_path(self, G,start, end, heuristic = None):
		if heuristic:
			return self.strategy(G, start, end, heuristic)
		return self.strategy(G, start, end)
