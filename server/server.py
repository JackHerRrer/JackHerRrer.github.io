import socketserver
import json
from datetime import datetime
import time

ACK = (chr(6)).encode()  # ASCII ACK (Acknowledge)
NAK = (chr(21)).encode()  # ASCII NAK (Not Acknowledged)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip().decode()

        if self.data != "{":
                self.request.sendall(NAK)
                print(' Not JSON.')
                return  # close connection

        # retrieve remaining json
        self.data = self.data + self.request.recv(1024).strip().decode()

        # convert string to dictionnary
        self.json_data = json.loads(self.data)
        self.date = round(time.time())
        print(f'Received at {datetime.now().strftime("%H:%M:%S")}')
        print(self.json_data)

        # acknowledge packet
        self.request.sendall(ACK)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9501

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f'server started on port:{PORT}')
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()