#!/usr/bin/env python
# Created by zahza at 3/11/20


import pickle
import os
import tqdm
from detector import GuiDetector
import cv2 as cv
from audio import AudioStream
import socket
from PIL import Image
import webbrowser

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


class ServerHandler:
	"""
	The ServerHandler class processes requests sent by the ServerHandler class
	"""

	def __init__(self, client_socket, client_address):
		"""
		ServerHandler constructor
		@param client_socket: TCP socket
		@param client_address: TCP Address
		"""
		self.client_socket = client_socket
		self.client_address = client_address
		self.button_coordinates = None
		self.text_field_coordinates = None

		self.microphone = AudioStream(5)

	def request_screenshot(self):
		"""
		Sends request to a computer (via TCP sockets) to perform a screen capture of the desktop screen.
		"""
		print(f"[+] Requesting screenshot from {self.client_address}")
		# Send request
		self.client_socket.send(pickle.dumps("CAPTURE_SCREEN"))
		# Receive response from computer
		response = self.client_socket.recv(BUFFER_SIZE).decode()
		filename, file_size = response.split(SEPARATOR)

		filename = os.path.basename(filename)

		file_size = int(file_size)
		progress = tqdm.tqdm(range(file_size), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		# Upload and save .png file
		with open(filename, "wb") as f:
			for _ in progress:
				try:
					bytes_read = self.client_socket.recv(BUFFER_SIZE)
					f.write(bytes_read)
					# If no more bytes to read
					if not bytes_read:
						f.close()
						break
				# Socket isn't sending anything else
				except:
					f.close()
					break

				progress.update(len(bytes_read))
		print(f"[+] Sending file confirmation to {self.client_address}")
		self.client_socket.send(pickle.dumps("FILE_UPLOAD_RECEIVED"))

	def request_mouse_movement(self, coordinates, flag: int):
		"""
		Sends request to computer to mouse its mouse
		"""
		print(f"[+] Requesting mouse movement from {self.client_address}")
		self.client_socket.send(pickle.dumps(["MOVE_MOUSE", coordinates, flag]))

	def request_keyboard_typing(self, keyboard_text: str):
		"""
		Sends request to computer to type with its keyboard
		"""
		print(f"[+] Requesting keyboard typing from {self.client_address}")
		self.client_socket.send(pickle.dumps(["TYPE_WITH_KEYBOARD", keyboard_text]))

	def request_picture(self):
		print(f"[+] Requesting picture typing from {self.client_address}")
		self.client_socket.send(pickle.dumps("SHOW_PICTURE"))

	def call_on_assistant(self):
		"""
		Resumes conversation with Google's DialogFlow Chatbot. Process client requests based on Chatbot's responses
		"""
		# self.request_screenshot()
		# self.find_gui_objects()
		self.microphone.speak_text("What would you like to do?")
		voice_command = self.microphone.record_voice()
		print("User Said: " + voice_command)
		assistant_response = AudioStream.detect_intent_texts(voice_command)
		AudioStream.speak_text(assistant_response)

		# 1. User: "Log me into my account"
		if "Alright. Lets log you in. What is your username?" in assistant_response:
			self.fill_information()
		# 2. User: "Lets create a new patient record"/ "Lets add another patient record."
		elif "Alright, what is the patient's name?" in assistant_response:
			self.fill_information()

		elif "Alright, accessing Rodger's patient chart." in assistant_response:
			self.get_patient_chart()

		elif "Ok. Retrieving Rodger's latest wound image." in assistant_response:
			self.request_picture()

	def get_patient_chart(self):
		print(f"[+] Requesting picture typing from {self.client_address}")
		self.client_socket.send(pickle.dumps("GET_CHART"))

	def fill_information(self):
		for i in range(len(self.text_field_coordinates)):
			print(self.text_field_coordinates[i])
			voice_reply = self.microphone.record_voice()
			print("User Said: " + voice_reply)
			self.request_mouse_movement(self.text_field_coordinates[i], 0)
			self.request_keyboard_typing(voice_reply)

			assistant_response = AudioStream.detect_intent_texts(voice_reply)
			AudioStream.speak_text(assistant_response)

		# Login Button
		if len(self.button_coordinates) == 1:
			self.request_mouse_movement(self.button_coordinates[0], 1)
		# Add Button
		else:
			self.request_mouse_movement(self.button_coordinates[0], 1)

		print(f"[+] Finished filling information for {self.client_address}")
		self.client_socket.send(pickle.dumps("FILLING_INFORMATION_COMPLETE"))

	def find_gui_objects(self):
		"""
		Detects and returns buttons and text fields coordinates found in desktop screen image.
		"""
		frame = cv.imread("desktop_image.png")
		button_objects = GuiDetector.detect_gui_objects(frame, 5, 500, 900)
		self.button_coordinates = GuiDetector.find_centers(button_objects)

		textfield_objects = GuiDetector.detect_gui_objects(frame, 50, 1000, 9000)

		self.text_field_coordinates = GuiDetector.find_centers(textfield_objects)
		print(f"[+] Completed analyzing gui for {self.client_address}")
		self.client_socket.send(pickle.dumps("FOUND_GUI_COMPLETE"))


class ClientHandler:
	"""
	ClientHandler class processes requests sent by the server
	"""

	def __init__(self, client_socket, client_address):
		"""
		ClientHandler Constructor
		@param client_socket: Server TCP Socket
		@param client_address: Server TCP Address
		"""
		self.client_socket = client_socket
		self.client_address = client_address
		from input import InputHandler
		# Initializes InputHandler class
		self.client_input = InputHandler()

	def type_with_keyboard(self, text: str):
		"""
		Types text received by the server into the computer. Once action is complete,
		client notifies the server of action conclusion.
		@param text: String message received by server
		"""
		self.client_input.control_keyboard(text)
		self.client_socket.send(pickle.dumps("KEYBOARD_TYPING_COMPLETE"))

	def move_mouse(self, coordinates: tuple, flag: int):
		"""
		Moves mouse using X/Y coordinates received by server.
		@param coordinates: X,Y pair received by server
		@param flag: Determines whether mouse action is over a button or text field.
		"""
		self.client_input.control_mouse(coordinates, flag)
		self.client_socket.send(pickle.dumps("MOUSE_MOVEMENT_COMPLETE"))

	def send_screenshot(self):
		"""
		Performs and sends desktop screen capture to server.
		"""
		self.client_input.take_screenshot()
		filename = "desktop_image.png"
		file_size = os.path.getsize(filename)

		# Sending File to Server
		print(f"[+] Sending screen to {self.client_address}")
		self.client_socket.send(f"{filename}{SEPARATOR}{file_size}".encode())
		progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		with open(filename, "rb") as f:
			for _ in progress:
				# read the bytes from the file
				bytes_read = f.read(BUFFER_SIZE)

				if not bytes_read:
					break

				self.client_socket.sendall(bytes_read)
				# update the progress bar
				progress.update(len(bytes_read))

	def resume_assistant(self):
		"""
		Sends request to server to resume conversation with assistant.
		"""
		print(f"[+] Resuming voice assistance services for {self.client_address}")
		self.client_socket.send(pickle.dumps("RESUME_ASSISTANT"))

	def analyze_desktop(self):
		print(f"[+] Start analyzing desktop for {self.client_address}")
		self.client_socket.send(pickle.dumps("FIND_GUI_OBJECTS"))

	def fill_information(self):
		print(f"[+] Start filling information for {self.client_address}")
		self.client_socket.send(pickle.dumps("FILL_INFORMATION"))

	def show_picture(self):
		img = Image.open("RodgerPeters_8923458345.jpg")
		img.show()

	def get_chart(self):
		webbrowser.open_new_tab("http://127.0.0.1:8000/#/")
		self.client_socket.send(pickle.dumps("RESUME_ASSISTANT"))
