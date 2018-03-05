def manhattan_distance(c1,c2):
	return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def euclidean_distance(c1,c2):
	return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)**.5

def chebyshev_distance(c1,c2):
	return max(abs(c1[0] - c2[1]), abs(c1[1] - c2[1]))