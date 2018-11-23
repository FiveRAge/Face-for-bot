# -*- coding: utf-8 -*-
from yandex_speech import TTS
import pygame
import rospy
import struct
from std_msgs.msg import String, Bool
import numpy as np
from time import sleep
import glob, os
import threading
mask = np.array(['у','е','ы','а','о','э','я','и','ю','ё',' ', '.'])
maskfase = np.array(['2','6','0','6','2','4','6','4','0','2','1','1'])
lenghtmusic = 0
FileName = ""


startplay = False
enable = False
text = ""
def play(data):
	global lenghtmusic
	#play speech.wav
	file = data
	pygame.init()
	pygame.mixer.init(frequency=48000)
	pygame.mixer.music.load("files/speech.wav")
	m = pygame.mixer.Sound("files/speech.wav")
	lenghtmusic = m.get_length()
	pygame.mixer.music.play()
	print lenghtmusic

def setFace(data):
	massface = []
	for arr in data:
		for simbol in arr.decode("utf-8"):
			simbol = simbol.encode('utf-8')
			if (simbol.lower() == mask).any():
				r  = [arr, maskfase[np.where(mask == simbol.lower())[0][0]]]
				massface.append(r)
				#print r
	massface.append([" ", 1])
	return massface
def reader(data):
	text = []
	mes = ''
	i = 0
	for a in data.decode("utf-8"):
		#print mask == a.lower().encode('utf-8')
		a = a.encode('utf-8')
		if not (mask == a.lower()).any():

			mes += a
		else:
			i += 1
			mes += a
			text.append(mes)
			mes = ""
	print i
	return text
def startanimation(data):
	while 1:
		global startplay
		if startplay:
			play(FileName)
			startplay = False
			break
	i = 0
	for arr in data:
		if (arr[0] == '.'):
			i+=1
	for arr in data:
		print "mouth_{}_{}".format(arr[1], 1)

		pub = rospy.Publisher("/display_chatter", String)
		pub.publish("mouth_{}_{}".format(arr[1], 1))
		if (arr[0] == '.'):
			sleep(0.4)
		else:
			sleep((lenghtmusic-(1.6*i))/len(data))


rospy.init_node('speech')
def getresult(data):
	global startplay
	print data
	startplay = True
def getfile(data):
	pass
def getmessage(data):
	pub = rospy.Publisher('/text2speech/text', String)
	print data.data
	pub.publish(data.data)
	print("send message")
	global text
	text = data.data
	data1 = setFace(reader(data.data))
	#print data1
	startanimation(data1)
	#startanimation(data1, True)
rospy.Subscriber('/animateText', String, getmessage)
rospy.Subscriber('/text2speech/result', Bool, getresult)
rospy.Subscriber('/text2speech/nameFile', String, getfile)
while not rospy.is_shutdown():
	pass
