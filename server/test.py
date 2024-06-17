import requests
import time
import json

# URL of the server
url = 'http://localhost:8008'

# Sending a GET request
start=time.time()
response_get = requests.get(url)
print('GET response:', (time.time()-start)*1000)
print(response_get.json())

# Data to be sent in the POST request
data = {
    'id':'002',
    'name': 'Jonas',
    'message': 'Hello, server!',
    'shots':[{'x':20,'y':30,'v':(20,30)}]
}

# Sending a POST request
start=time.time()
response_post = requests.post(url, json=data)
print('POST response:', (time.time()-start)*1000)
print(response_post.json())
