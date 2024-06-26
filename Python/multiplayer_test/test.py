import requests
import time
import json

# URL of the server
url = 'http://localhost:8008'

# Data to be sent in the POST request
data = {
    'id': '002',
    'name': 'Jonas',
    'position_w': [-500, 400],
    'position_p': [1000, 400],
    'shots': []
}

# Sending a POST request
start = time.time()
response_post = requests.post(url, json=data)
print('POST response:', (time.time() - start) * 1000)
print(response_post.json())