import requests


class server_client:

    def __init__(self) -> None:
        self.url = 'http://localhost:8008'
    # URL of the server
    
    def get(self):
        # Sending a GET request
        response_get = requests.get(self.url)
        return response_get.json()

    # Data to be sent in the POST request

    def post(self, id, position_w, position_p, shots=[]):
        # Sending a POST request
        data = {
            'id':id,
            'name': 'Jonas',
            'position_w':position_w,
            'position_p':position_p,
            'shots':shots
        }
        
        response_post = requests.post(self.url, json=data)
        return response_post.json()
