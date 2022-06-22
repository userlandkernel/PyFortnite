import os
import sys
import psutil
import subprocess
import errno
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import win32api, win32con, win32gui
import cv2
import pyautogui
import time
import math
import threading
import gtts
import playsound

INFINITE = -1
MINUTE = 60
    
class FortniteCheatEngine:

	def __init__(self, dataDir="hacker-engine-data/"):
		self.detector = hub.load("https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1")
		self.size_scale = 3
		self.dataDir = dataDir
		self.audioDir = self.dataDir+"/audio/"
		self.modelDir = self.dataDir+"/models/"

	def playAudio(self, name, text):
		if os.path.exists(self.audioDir+name):
			playsound.playsound(self.audioDir+name)
		else:
			tts = gtts.gTTS(text, lang="en")
			tts.save(self.audioDir+name)

	def isRunning(self):

		# Check if fortnite process is running
		print("Checking whether fortnite is already running...")
		for proc in psutil.process_iter():
			try:
				if 'fortnite' in proc.name().lower() or 'unrealwindow' in proc.name().lower():
					print("Found running game process!")
					return True
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				pass
		print("Did not find a running instance of fortnite.")	
		return False

	def waitForImage(self, name, timeout=30):
		tStart = time.time()
		image = pyautogui.locateOnScreen(self.modelDir+name)
		#Searches for the image
		while image == None:
			image = pyautogui.locateOnScreen(self.modelDir+name)
			if time.time() - tStart > timeout:
				print("Giving up, can't find image: "+name)
				return None
		return image

	def getImage(self, name):
		return pyautogui.locateOnScreen(self.modelDir+name)

	def playDeathrun(self):
		return True

	def performGameplayRoutine(self):

		print("Performing routine")

		# Join battle
		image = self.waitForImage('play-button2.png')
		if image == None:
			return False
		pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
		pyautogui.click()

		# Wait to exit the bus
		image = self.waitForImage('battlebus-laststop.png', 5*MINUTE)
		if image == None:
			print("Can't find last busstop section")

		# Thank bus driver and jump
		for i in range(0, 4):
			pyautogui.press('b') 
			pyautogui.press('space')
		#self.playAudio("exited-bus.mp3", "We exited the bus!")

		# Rage quit game
		pyautogui.press('esc')

		# Exit battle royale
		image = self.waitForImage('exit-battleroyale.png', 5*MINUTE)
		if image == None:
			return False
		pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
		pyautogui.click()


		# Return to lobby
		image = self.waitForImage('return-to-lobby.png', 5*MINUTE)
		if image == None:
			return False
		pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
		pyautogui.click()

		# Confirm
		image = self.waitForImage('yes-button.png', 5*MINUTE)
		if image == None:
			return False
		pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
		pyautogui.click()

		# Close any modal
		image = self.waitForImage('close-button.png', 20)
		if image != None:
			pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
			pyautogui.click()
		else:
			print("Cannot find close button")

		image = self.waitForImage('claim.png', 3)
		if image != None:
			pyautogui.moveTo(image.left+10, image.top+10, duration=0, tween=pyautogui.easeInOutQuad)
			pyautogui.click()

	def startGamePlay(self, attach=False, timeToPlay=INFINITE):


		# Note current time, for playing the amount of seconds in timeToPlay
		tStart = time.time()
		
		# Wait for lobby play button and click it
		#self.playAudio("lobby-play.mp3", "Waiting for lobby to appear")

		# Keep playing for the duration of timeToPlay (or infinitely)
		while time.time() - tStart < timeToPlay or timeToPlay == INFINITE:

			self.performGameplayRoutine()
			#self.playAudio("join-next.mp3", "Joining next game")


	def terminate(self):
		self.p.terminate()

	def runGame(self, attach=False):
		
		# Launch the game
		#self.playAudio("start-fortnite.mp3", "Starting Fortnite")

		if not attach:
			self.p = subprocess.Popen("C:/Program Files/Epic Games/Fortnite/FortniteGame/Binaries/Win64/FortniteClient-Win64-Shipping_EAC.exe")
			self.pOut = self.p.communicate()

		
		# Prepare gameplay
		self.startGamePlay(attach=attach)

if __name__ == "__main__":
	tf.test.is_gpu_available(cuda_only=True, min_cuda_compute_capability=None)
	engine = FortniteCheatEngine()
	engine.runGame(attach=engine.isRunning())
	engine.terminate()
