#!/usr/bin/env python
'''
MSER detector demo
==================
Usage:
------
    mser.py [<video source>]
Keys:
-----
    ESC   - exit
'''

# Python 2/3 compatibility

import cv2 as cv


class GuiDetector:
	"""
	The GuiDetector class uses the OpenCV library to detect buttons and text fields in
	Graphic User Interfaces.
	"""

	# 5/500/900 Buttons
	# 50/1000/9000 Text fields
	@staticmethod
	def detect_gui_objects(image, delta, min_area, max_area):
		"""

		@param image:
		@param delta:
		@param min_area:
		@param max_area:
		@return:
		"""
		gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
		mser_objects = cv.MSER_create(_delta=delta,
									  _max_variation=0.0003,
									  _min_area=min_area,
									  _max_area=max_area)
		regions, bboxes = mser_objects.detectRegions(gray)
		hulls = [cv.convexHull(p) for p in regions]
		return hulls

	@staticmethod
	def find_centers(hulls):
		coordinates = []
		for i in hulls:
			m = cv.moments(i)
			try:
				cx = int(m["m10"] / m["m00"])
				cy = int(m["m01"] / m["m00"])
				coord = (cx, cy)
				coordinates.append(coord)
			except:
				pass
		coordinates.sort()
		return coordinates

	@staticmethod
	def draw_objects(img, coordinates):
		for i in coordinates:
			cv.circle(img, (i[0], i[1]), 7, (0, 0, 0), -1)
			cv.putText(img, "center", (i[0] - 20, i[1] - 20),
					   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
