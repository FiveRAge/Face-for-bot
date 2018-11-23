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
text = ""
i = 0
startplay = False
enable = False
text = ""
def generate():
	while not rospy.is_shutdown():
		global text
		global enable
		if enable:
			tts = TTS("zahar", "wav", "4b48f713-4f62-438e-aac9-45bcf062ec3d")
			tts.generate(text)
			tts.save()
			print("save data")
			enable = False
			pub = rospy.Publisher('/text2speech/result', Bool)
			pub.publish(True)

t1 = threading.Thread(target=generate)
t1.start()
def getmessage(data):
	global text
	global enable
	print data.data
	text= data.data
	enable = True
rospy.init_node('speech1')
#def getmessage(data):
#text1 = "Не следует, однако, зывать о том, что рамки и место обучения кадров создаёт предпосылки качественно новых шагов для форм воздействия. Равным образом дальнейшее развитие различных форм деятельности требует от нас анализа дальнейших направлений развитая системы массового участия. Дорогие друзья, рамки и место обучения кадров в значительной степени обуславливает создание ключевых компонентов планируемого обновления"
#	text = data.data
#	print type(text1)


rospy.Subscriber('/text2speech/text', String, getmessage)
while not rospy.is_shutdown():
	pass
