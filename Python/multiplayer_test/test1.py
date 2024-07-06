import threading
import socket
from socket_client_server import SocketClientServer  # Angenommen, die Klasse ist in einer Datei namens socket_client_server.py gespeichert

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def start_server():
    server_ip = get_local_ip()
    server = SocketClientServer(host=server_ip, port=8009, broadcast_port=9001)
    print(f"Server IP address: {server_ip}")
    server.start_server()
    return server

if __name__ == "__main__":
    # Starte den Server in einem separaten Thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Warte, bis der Server-Thread beendet ist
    server_thread.join()
