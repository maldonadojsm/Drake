#!/usr/bin/env python
# Created by zahza at 4/2/20
"""Enter Script Description Here"""

from detector import GuiDetector
import cv2 as cv
import argparse
import pyautogui

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picture", required=True, help=".png image")

args = vars(ap.parse_args())

frame = cv.imread(args['picture'])
button_objects = GuiDetector.detect_gui_objects(frame, 5, 500, 900)
button_coordinates = GuiDetector.find_centers(button_objects)
GuiDetector.draw_objects(frame, button_coordinates)

textfield_objects = GuiDetector.detect_gui_objects(frame, 50, 1000, 9000)  # 3000/9000 works for leads page

textfield_coordinates = GuiDetector.find_centers(textfield_objects)
GuiDetector.draw_objects(frame, textfield_coordinates)
cv.polylines(frame, button_objects, 1, (0, 255, 0))
cv.polylines(frame, textfield_objects, 1, (0, 255, 0))
print(len(button_coordinates))
print(len(textfield_coordinates))
cv.imshow('img', frame)
cv.waitKey(0)
