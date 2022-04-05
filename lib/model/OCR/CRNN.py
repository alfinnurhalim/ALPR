import cv2
import torch
import numpy as np

import easyocr as ocr

from lib.model.Model import Model

class CRNN(Model):
	def __init__(self,language = ['en',]):
		self.language = language
		self.reader = None

		self.min_coonfidence = 0.5

	def load_model(self):
		self.reader = ocr.Reader(self.language)

	def run(self,img):
		text = self.reader.readtext(img)

		if len(text) > 0:
			text = max(text, key=lambda x: x[-1])
			text = text[-2:] if text[-1] > self.min_coonfidence else list()

		return text