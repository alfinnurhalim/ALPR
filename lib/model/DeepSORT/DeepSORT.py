import cv2
import torch
import numpy as np

from lib.model.Model import Model
from lib.model.DeepSORT.SORT import Sort

class DeepSORT(Model):
	def __init__(self,max_age=90,min_hits=3,override_track_class=False):

		self.max_age = max_age 
		self.min_hits = min_hits
		self.override_track_class=override_track_class
		self.tracker = None

	def load_model(self):
		self.tracker = Sort(max_age=self.max_age, 
							min_hits=self.min_hits)

	def run(self,img,labels):
		track_input = list()

		for label in labels:
			x1,y1,w,h = label[0]
			score = label[1]

			x2 = x1 + w
			y2 = y1 + h

			track_input.append([x1,y1,x2,y2,score])

		result = []

		tracks = self.tracker.update(np.array(track_input))
		for track in tracks:
			track = track.astype(int).tolist()

			x1,y1,x2,y2,ids = track
			w = int(abs(x2-x1))
			h = int(abs(y2-y1))

			result.append([[x1,y1,w,h],ids])
		return result