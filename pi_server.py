import socket
import argparse
from audio import AudioStream
from listener import ServerListener
import pickle

# Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--server_ip", required=True, help="IP Address of Server")
ap.add_argument("-p", "--port_number", required=True, help="Port Number of Server")

args = vars(ap.parse_args())
# Create Sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_HOST = args["server_ip"]
SERVER_PORT = int(args["port_number"])
# Bind socket to device's IP and PORT
try:
	server_socket.bind((SERVER_HOST, SERVER_PORT))
except socket.error:
	print('Bind Failed')
	exit(0)

# Listen to N clients
N = 1
server_socket.listen(N)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
# Accepting Client's connections.
(client_socket, client_addr) = server_socket.accept()
# Allow a socket to timeout for at most 2 seconds.
client_socket.settimeout(2)

print(f"[+] {client_addr} is connected.")
# Initialize server listener
server_listener = ServerListener(client_socket, client_addr)

# Start conversation with voice assistant.

AudioStream.speak_text("Hello! I'm Surg On. You're personal E H R Assistant")

# Call on Voice Assistant
server_listener.server_handler.call_on_assistant()

while True:
	data = client_socket.recv(1024)
	client_response = pickle.loads(data)
	print("CLIENT SAID: " + client_response)
	server_listener.on_receiving_client_response(client_response)
