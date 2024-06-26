from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi

# In-Memory storage for received data
stored_data = []

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        response = {'stored_data': stored_data, 'received': 'ok'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('Content-Length'))
        message = json.loads(self.rfile.read(length).decode('utf-8'))

        existing = False
        for index, d in enumerate(stored_data):
            if d['id'] == message['id']:
                stored_data[index] = message
                existing = True

        if not existing:
            stored_data.append(message)

        # send the message back
        self._set_headers()
        response = {'stored_data': stored_data, 'received': 'ok'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()