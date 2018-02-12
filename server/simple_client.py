
import requests


if __name__ =="__main__":

	#Server Host
	base_url = "http://localhost"

	#Files to be sent over post request
	files = {"image": open("maze.png", 'rb')}

	#Post request response
	response = requests.post(base_url + "/solve", files=files)