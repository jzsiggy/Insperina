import cv2
from imutils.video import VideoStream
import imutils
import random
import os
import time
from train_model import train_model
from extract_embeddings import extract_embeddings
from recognize_video import load_detector



name=input('Digite seu nome: ')

vs = VideoStream(0).start()	#COMPUTERCAM
# vs = VideoStream('http://10.92.129.143:8888/video').start()	#IPCAM
time.sleep(2.0)
# fps = FPS().start()


path='dataset/{}'.format(name)

while os.path.exists(path):
	print('Nome já cadastrado.')
	name=input('qual nome? ')
	path='dataset/{}'.format(name)

os.mkdir(path)

i=0

while i<60:
	i+=1
	frame = vs.read()
	cv2.imwrite(os.path.join(path,  '{}_{}.png'.format(name,i)),  frame)
	print(i)
	time.sleep(0.1)
new_dir = True

vs.stop()


extract_embeddings()
train_model()
load_detector()







