from collections import deque

def bfs(maze):

	seen = set()
	start = maze.start 
	seen.add(start)
	frontier = deque([start])

	while len(frontier) > 0:
		current_node = frontier.popleft()
		seen.add(current_node)
		
		if current_node == maze.end:
			return True

		for neighbor in current_node.children:
			if neighbor in seen:
				continue
			seen.add(neighbor)
	return False