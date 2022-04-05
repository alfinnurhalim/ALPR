import numpy as np
import pandas as pd


class Model(object):
 	def __init__(self, name):
 		self.name = name

 	def load_model(self):
 		raise NotImplementedError
 	
 	def run(self):
 		raise NotImplementedError
