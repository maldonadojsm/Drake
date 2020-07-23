# USAGE
# python object_detector.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel
# --montageW 2
# --montageH 2

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import cv2 as cv
import time
import imutils
from imutils.video import VideoStream
from imutils import build_montages
from detector import GuiDetector
import os

os.environ['DISPLAY'] = ':0'
# construct the argument parser and parse the arguments
vs = VideoStream(usePiCamera=1, resolution=(1680, 1050)).start()
time.sleep(2)
mW = 1
mH = 1

while True:
	# frame = vs.read()
	#	(h, w) = frame.shape[:2]
	frame = cv.imread("desktop_image.png")
	button_objects = GuiDetector.detect_gui_objects(frame, 5, 500, 900)

	button_coordinates = GuiDetector.find_centers(button_objects)
	GuiDetector.draw_objects(frame, button_coordinates)

	textfield_objects = GuiDetector.detect_gui_objects(frame, 50, 1000, 9000)

	textfield_coordinates = GuiDetector.find_centers(textfield_objects)
	GuiDetector.draw_objects(frame, textfield_coordinates)
	cv.polylines(frame, button_objects, 1, (0, 255, 0))

	cv.polylines(frame, textfield_objects, 1, (0, 255, 0))
	#	frameDict['pi4'] = frame
	#	montages = build_montages(frameDict.values(), (w, h), (mW, mH))

	#	for (i, montage) in enumerate(montages):
	#		cv.imshow('img', montage)
	#		cv.waitKey(1)
	#
	print(button_coordinates)
	print(textfield_coordinates)
	cv.imshow('img', frame)
	cv.waitKey(1)

cv.destroyAllWindows()
