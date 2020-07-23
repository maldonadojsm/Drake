#!/usr/bin/env python
# Created by zahza at 3/23/20
"""Enter Script Description Here"""
from audio import AudioStream
from video import VideoStream
from handler import ClientHandler, ServerHandler


class ServerListener:
	"""
	The ServerListener class waits for requests sent from the client and relays them to the handler class.
	"""

	def __init__(self, client_socket, client_address):
		"""
		ServerListener Constructor
		@param client_socket: Client's TCP socket
		@param client_address: Client's IP address
		"""
		self.server_handler = ServerHandler(client_socket, client_address)

	@staticmethod
	def start_video_stream(server_ip, server_port):
		"""
		FUNCTIONING BUT NOT INTEGRATED WITHIN WORKFLOW
		Starts video stream between client and server using UDP.
		@param server_ip: Server's IP
		@param server_port: Server's Port Number
		"""
		# start video stream
		VideoStream.initialize_video_stream(server_ip, server_port)

	def on_receiving_client_response(self, response: str):
		"""
		Relays actions to the handler class based on responses received by the client.
		@param response: Client response in string format.
		"""
		if "FILE_UPLOAD_COMPLETE" in response:
			self.server_handler.find_gui_objects()

		elif "FIND_GUI_OBJECTS" in response:
			self.server_handler.find_gui_objects()

		elif "FILL_INFORMATION" in response:
			self.server_handler.call_on_assistant()

		elif "RESUME_ASSISTANT" in response:
			self.server_handler.call_on_assistant()

	@staticmethod
	def start_audio_stream(server_ip, server_port, recording_duration: int):
		"""
		FUNCTIONING BUT NOT INTEGRATED WITHIN WORKFLOW.
		Starts audio stream between the server and the client.
		@param server_ip: Server's IP
		@param server_port: Server's Port
		@param recording_duration: Duration of performed recordings.
		"""
		audio = AudioStream.record_voice(recording_duration)
		AudioStream.write_audio_file(audio)
		AudioStream.send_audio_file(server_ip, server_port)

	def on_receive_audio_file(self, audio_file):
		"""
		FUNCTIONING BUT NOT INTEGRATED WITHIN WORKFLOW.
		Receives and plays MP3 received by server.
		@param audio_file: Audio File in MP3 format.
		"""
		self.audio_stream.play_audio_file(audio_file)


class ClientListener:
	"""
	The ClientListener class waits and processes requests send by the server.
	"""

	def __init__(self, server_socket, server_address):
		"""
		ClientListener Constructor
		@param server_socket: Server's TCP Socket
		@param server_address: Server's IP Address
		"""
		self.client_handler = ClientHandler(server_socket, server_address)

	def on_receiving_server_response(self, response: list):
		"""
		Relays actions to handler class depending on the responses sent by the server.
		@param response: List containing either a server response or a pair of coordinates and server response.
		"""
		if "CAPTURE_SCREEN" in response:
			self.client_handler.send_screenshot()

		elif "FILE_UPLOAD_RECEIVED" in response:
			self.client_handler.analyze_desktop()

		elif "MOVE_MOUSE" in response[0]:
			self.client_handler.move_mouse(response[1], response[2])

		elif "TYPE_WITH_KEYBOARD" in response[0]:
			self.client_handler.type_with_keyboard(response[1])

		elif "FILLING_INFORMATION_COMPLETE" in response:
			self.client_handler.resume_assistant()

		elif "FOUND_GUI_COMPLETE" in response:
			self.client_handler.fill_information()

		elif "SHOW_PICTURE" in response:
			self.client_handler.show_picture()

		elif "GET_CHART" in response:
			self.client_handler.get_chart()
