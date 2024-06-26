import requests
import time
import json

class server_client:

    def __init__(self) -> None:
        self.url = 'http://localhost:8008'
    # URL of the server
    
    def get(self):
        # Sending a GET request
        response_get = requests.get(self.url)
        return response_get.json()

    # Data to be sent in the POST request

    def post(url, data):
        # Sending a POST request
        response_post = requests.post(url, json=data)
        return response_post.json()
