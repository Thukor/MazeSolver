
import requests


if __name__ =="__main__":

	#Server Host
	base_url = "http://72.224.10.212:8080"

	#Files to be sent over post request
	files = {"image": open("maze.png", 'rb')}

	#Post request response
	response = requests.get(base_url + "/hello1")
