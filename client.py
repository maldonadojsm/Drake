import socket
import pickle
from listener import ClientListener
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-ip", "--server_ip", required=True, help="IP Address of Server")
ap.add_argument("-p", "--port_number", required=True, help="Port Number of Server")

args = vars(ap.parse_args())

SERVER_HOST = args["server_ip"]
SERVER_PORT = int(args["port_number"])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
server_socket.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
client_listener = ClientListener(server_socket, SERVER_HOST)
while True:
	data = server_socket.recv(1024)
	server_response = pickle.loads(data)
	try:
		print("SERVER SAID: " + server_response)
		client_listener.on_receiving_server_response(server_response)
	except:
		print("SERVER SAID: " + server_response[0])
		client_listener.on_receiving_server_response(server_response)
