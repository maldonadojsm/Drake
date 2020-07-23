#!/usr/bin/env python
# Created by zahza at 3/22/20
"""Enter Script Description Here"""

import imagezmq
import imutils.video
import socket


class VideoStream:
	"""
	The VideoRecorder class establishes a video stream between the Pi Camera / USB Camera and server.
	"""

	@staticmethod
	def initialize_video_stream(server_ip, server_port):
		"""
		Creates, prepares and starts video stream
		"""
		sender = imagezmq.ImageSender(connect_to="tcp://{}:{}".format(server_ip, server_port))
		# Get client hostname
		client_hostname = socket.gethostname()
		# Start Camera
		video_stream = imutils.video.VideoStream(src=0).start()
		# video_stream = imutils.video.VideoStream(usePiCamera=True, resolution=(320, 240)).start()

		# read frame from camera and send to server
		while True:
			frame = video_stream.read()
			sender.send_image(client_hostname, frame)
