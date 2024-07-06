# import requests
# import time
# import json

# # URL of the server
# url = 'http://localhost:8009'

# # Data to be sent in the POST request
# data = {
#     'id': '002',
#     'name': 'Jonas',
#     'position_w': [-500, 400],
#     'position_p': [1000, 400],
#     'shots': []
# }

# # Sending a POST request
# start = time.time()
# response_post = requests.post(url, json=data)
# print('POST response:', (time.time() - start) * 1000)
# print(response_post.json())



# response_post = requests.delete(url, json=data)
# print(response_post.json())


import threading
import time
from socket_client_server import SocketClientServer  # Angenommen, die Klasse ist in einer Datei namens socket_client_server.py gespeichert

# Funktion zum Starten des Servers
def start_server():
    server = SocketClientServer(host='127.0.0.1', port=8009, broadcast_port=9000)
    server.start_server()
    return server

# Funktion zum Starten des Clients
def start_client():
    client = SocketClientServer()
    server_address = client.discover_servers()
    if server_address:
        server_host, server_port = server_address.split(':')
        client.connect_to_server(server_host, int(server_port))
        return client
    else:
        print("No server found")
        return None

# Hauptteil des Tests
if __name__ == "__main__":
    # Starte den Server in einem separaten Thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Warte kurz, um sicherzustellen, dass der Server gestartet ist
    time.sleep(2)

    # Starte den Client und verbinde mit dem Server
    client = start_client()

    if client:
        # Warte eine kurze Zeit, um sicherzustellen, dass die Verbindung hergestellt wurde
        time.sleep(1)

        # Testnachricht senden
        test_data = {"action": "test", "message": "Hello, Server!"}
        response = client.send(test_data)
        print(f"Client received response: {response}")

        # Verbindung schließen
        client.close_connection()

    # Warte, bis der Server-Thread beendet ist
    server_thread.join()
