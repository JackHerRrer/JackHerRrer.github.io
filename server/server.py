import socketserver
import socket
import json
from datetime import datetime
import time
import gspread
from google.oauth2.service_account import Credentials

import logging
import os
from systemd.journal import JournalHandler

# Add a logger 
logger = logging.getLogger(__name__)
journalHandler = JournalHandler(SYSLOG_IDENTIFIER='iSpindleServer')
# Initially set to log all - change this in production
logger.setLevel(logging.DEBUG)
logger.addHandler(journalHandler)

ACK = (chr(6)).encode()  # ASCII ACK (Acknowledge)
NAK = (chr(21)).encode()  # ASCII NAK (Not Acknowledged)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("/home/pi/iSpindleServer/server/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

workbook_id = "1aS_RncSOZyQ2PjkBUbK2wP3NuweIIooTjVOnxhCtmzk"
workbook = client.open_by_key(workbook_id)
current_sheet = workbook.sheet1

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
                    logger.info("Inactivité détectée (timeout).")
                    break
                except (ConnectionResetError, BrokenPipeError):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Connexion coupée (probablement via SO_KEEPALIVE).")
                    logger.info("Connexion coupée (probablement via SO_KEEPALIVE).")
                    break

            # tentative de parsing JSON
            if self.data:
                try:
                    self.json_data = json.loads(self.data)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] JSON reçu :")
                    print(self.json_data)
                    logger.info(self.json_data)
                    self.request.sendall(ACK)

                    row_values=[
                        datetime.now().strftime('%m/%d/%Y %H:%M:%S'), 
                        self.json_data['gravity'] * 1000, 
                        self.json_data['temperature'], 
                        self.json_data['battery']
                    ]
                    current_sheet.append_row(row_values, value_input_option='USER_ENTERED')


                except json.JSONDecodeError:
                    print(f"[{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}] JSON invalide: {self.data}")
                    logger.info(f"JSON invalide: {self.data}")
                    self.request.sendall(NAK)



        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erreur inattendue : {e}")
            logger.info(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9501

    # Version mono-thread (simple)
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.allow_reuse_address = True  # important pour éviter TIME_WAIT
        print(f'Server started on port: {PORT}')
        logger.info(f'Server started on port: {PORT}')
        server.serve_forever()
