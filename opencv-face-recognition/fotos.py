import cv2
from imutils.video import VideoStream
import imutils
import random
import os
import time

name=input('qual nome? ')

vs = VideoStream(0).start()	#COMPUTERCAM
# vs = VideoStream('http://10.92.129.143:8888/video').start()	#IPCAM
time.sleep(2.0)
# fps = FPS().start()

path='../dataset/{}'.format(name)

while os.path.exists(path):
	print('Use outro nome pfvr')
	name=input('qual nome? ')
	path='../dataset/{}'.format(name)

os.mkdir(path)

i=0

while i<10:
	i+=1
	frame = vs.read()
	cv2.imwrite(os.path.join(path,  'zsig{}.png'.format(i)),  frame)
	print(i)
	time.sleep(0.1)

vs.stop()

