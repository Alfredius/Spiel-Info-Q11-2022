import time
from socket_client_server import SocketClientServer  # Angenommen, die Klasse ist in einer Datei namens socket_client_server.py gespeichert

def start_client(server_ip):
    client = SocketClientServer(broadcast_port=9001)  # Stellen Sie sicher, dass der gleiche Broadcast-Port verwendet wird
    client.connect_to_server(server_ip, 8009)
    return client

if __name__ == "__main__":
    # Geben Sie die IP-Adresse des Server-Laptops ein
    server_ip = input("Enter the server IP address: ")

    # Starte den Client und verbinde mit dem Server
    client = start_client(server_ip)

    if client:
        # Warte eine kurze Zeit, um sicherzustellen, dass die Verbindung hergestellt wurde
        time.sleep(1)

        # Testnachricht senden
        test_data = {"action": "test", "message": "Hello, Server!"}
        response = client.send(test_data)
        print(f"Client received response: {response}")

        # Verbindung schließen
        client.close_connection()
