import socketserver
import socket
import json
from datetime import datetime
import time

ACK = (chr(6)).encode()  # ASCII ACK (Acknowledge)
NAK = (chr(21)).encode()  # ASCII NAK (Not Acknowledged)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Request handler that reads a full JSON message from the client,
    applies TCP options, and replies with ACK or NAK.
    """

    def setup(self):
        # Setup est appelée avant handle() dans socketserver
        # Configuration des options TCP
        sock = self.request
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
        sock.settimeout(15)  # 15 secondes sans activité = timeout

    def handle(self):
        self.data = ""
        try:
            while True:
                try:
                    chunk = self.request.recv(4096)
                    if not chunk:
                        # the client closed the connection
                        break
                    self.data += chunk.decode()
                except socket.timeout:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Inactivité détectée (timeout).")
                    break
                except (ConnectionResetError, BrokenPipeError):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Connexion coupée (probablement via SO_KEEPALIVE).")
                    break

            # tentative de parsing JSON
            if self.data:
                try:
                    self.json_data = json.loads(self.data)
                    self.date = round(time.time())
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] JSON reçu :")
                    print(self.json_data)
                    self.request.sendall(ACK)
                except json.JSONDecodeError:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] JSON invalide")
                    self.request.sendall(NAK)

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur inattendue : {e}")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9501

    # Version mono-thread (simple)
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.allow_reuse_address = True  # important pour éviter TIME_WAIT
        print(f'Server started on port: {PORT}')
        server.serve_forever()
