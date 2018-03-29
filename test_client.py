import requests


#Server Host
base_url = "http://localhost"

#Files to be sent over post request
files = {"image": open("tiny_maze.png", 'rb')}

#Post request response
response = requests.post(base_url + "/demo", files=files)

with open("maze_graph.png", 'wb') as ms:
	ms.write(response.content)

