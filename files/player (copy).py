# -*- coding: utf-8 -*-
from yandex_speech import TTS
import pygame
import rospy
import struct
from std_msgs.msg import String
import numpy as np
from time import sleep
import glob, os

def generate(data):
	tts = TTS("zahar", "wav", "4b48f713-4f62-438e-aac9-45bcf062ec3d")
	tts.generate(data)
	tts.save()
	print("save data")
	#play()data[:20]
	return True
rospy.init_node('speech1')
def getmessage(data):
	print data.data
	generate(data.data)
rospy.Subscriber('/text2speech', String, getmessage)
