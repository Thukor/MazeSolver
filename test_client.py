import requests


#Server Host
base_url = "http://72.224.10.212:8080"

#Files to be sent over post request
files = {"image": open("tiny_maze.png", 'rb')}

#Post request response
response = requests.post(base_url + "/demo", files=files)

with open("maze_graph.png", 'wb') as ms:
	ms.write(response.content)

