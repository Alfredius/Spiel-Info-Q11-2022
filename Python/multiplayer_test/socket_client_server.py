import socket
import json
import threading

class SocketClientServer:
    def __init__(self, host='0.0.0.0', port=8009, broadcast_port=9000):
        self.host = host
        self.port = port
        self.broadcast_port = broadcast_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_found = None
        self.conn = None
        self.addr = None
        self.is_server = False
        self.client_connected = threading.Event()  # Event to signal client connection

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.is_server = True
        print(f'Server started at {self.host}:{self.port}')
        threading.Thread(target=self.listen_for_broadcasts).start()
        threading.Thread(target=self.wait_for_client).start()

    def wait_for_client(self):
        self.conn, self.addr = self.sock.accept()
        self.client_connected.set()  # Signal that a client has connected
        print(f'Connected by {self.addr}')
        self.handle_client()

    def listen_for_broadcasts(self):
        self.broadcast_sock.bind(('', self.broadcast_port))
        while True:
            data, addr = self.broadcast_sock.recvfrom(1024)
            if data.decode('utf-8') == 'DISCOVER_SERVER':
                self.broadcast_sock.sendto(f'SERVER_AT:{self.host}:{self.port}'.encode('utf-8'), addr)

    def handle_client(self):
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                response = self.handle_request(data)
                self.conn.sendall(response)

    def connect_to_server(self, server_host, server_port):
        self.sock.connect((server_host, server_port))
        print(f'Connected to server at {server_host}:{server_port}')

    def discover_servers(self, timeout=5):
        self.broadcast_sock.settimeout(timeout)
        self.broadcast_sock.sendto('DISCOVER_SERVER'.encode('utf-8'), ('<broadcast>', self.broadcast_port))
        try:
            while True:
                data, addr = self.broadcast_sock.recvfrom(1024)
                message = data.decode('utf-8')
                if message.startswith('SERVER_AT:'):
                    self.server_found = message.split('SERVER_AT:')[1]
                    break
        except socket.timeout:
            pass
        return self.server_found

    def handle_request(self, data):
        request = json.loads(data.decode('utf-8'))
        response = json.dumps({"status": "received", "data": request})
        return response.encode('utf-8')

    def send(self, data):
        json_data = json.dumps(data).encode('utf-8')
        if self.is_server and self.conn:
            try:
                self.conn.sendall(json_data)
                response = self.conn.recv(1024)
                return json.loads(response.decode('utf-8'))
            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Client disconnected")
                self.conn = None
                return {"status": "error", "message": "Client disconnected"}
        else:
            try:
                self.sock.sendall(json_data)
                response = self.sock.recv(1024)
                return json.loads(response.decode('utf-8'))
            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Server not connected")
                return {"status": "error", "message": "Server not connected"}

    def close_connection(self):
        if self.conn:
            self.conn.close()
        self.sock.close()
        print('Connection closed')
