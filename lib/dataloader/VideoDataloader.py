import cv2

class VideoLoader(object):
	def __init__(self, path, max_frame=None):
		self.cap = cv2.VideoCapture(path)
		self.frames = max_frame if max_frame != None else int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
		self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

		self.idx = 0
	def __iter__(self):
		return self

	def __next__(self):
		success, img = self.cap.read()
		self.idx += 1
		if not success or self.idx >= self.frames:
			self.idx = 0
			raise StopIteration

		return img

	def __len__(self):
		return self.frames 

class VideoWriter(object):
	def __init__(self, path):
		self.path = path
		self.writer = None

	def init_from_videoloader(self,data):
		fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
		self.writer = cv2.VideoWriter(self.path, fourcc, data.fps, (data.width, data.height))

	def update(self,img):
		self.writer.write(img)