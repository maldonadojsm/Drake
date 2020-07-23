#!/usr/bin/env python
# Created by zahza at 3/11/20

import pyautogui


class InputHandler:
	"""
	The Input Handler class processes automated mouse and keyboard input using the PyAutoGUI library.
	"""

	@staticmethod
	def control_mouse(coordinates: tuple, flag: int):
		"""
		Controls mouse using X/Y coordinates
		@param coordinates: tuple object (0 = x, 1 = y)
		@param flag: determines whether mouse action is over a button or text field
		"""
		# PyAuto GUI requires a dragRel call to enter information into text fields
		if flag == 0:
			pyautogui.moveTo(coordinates[0], coordinates[1])
			# We have to do just given otherwise we can't enter text into boxes
			pyautogui.dragRel(1, 1, duration=1, button='left')
			pyautogui.click(coordinates[0], coordinates[1])
		if flag == 1:
			pyautogui.moveTo(coordinates[0], coordinates[1])
			pyautogui.click(coordinates[0], coordinates[1])

	@staticmethod
	def control_keyboard(keyboard_message: str):
		"""
		Controls keyboard, types and processes message sent from temp
		@param keyboard_message: string message returned from Google Speech API (AWS)
		"""
		pyautogui.write(keyboard_message)
		pyautogui.press('Enter')

	@staticmethod
	def take_screenshot():
		image = pyautogui.screenshot()
		image.save('desktop_image.png')
