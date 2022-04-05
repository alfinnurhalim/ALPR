import cv2
import torch

from lib.model.Model import Model

class YOLO(Model):
	def __init__(self,):
		self.class_names = ['person','bicycle','car','motorbike','aeroplane','bus','train','truck','boat','traffic light','fire hydrant','stop sign','parking meter',
							'bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee','skis',
							'snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon',
							'bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','sofa','pottedplant','bed','diningtable','toilet',
							'tvmonitor','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear',
							'hair drier','toothbrush']

		self.class_interest = ['car','truck','motorbike',]
		self.min_coonfidence = 0.5

		self.model = None

	def load_model(self,model_path=None,hub='yolov5s'):
		if model_path == None:
			self.model = torch.hub.load('ultralytics/yolov5', hub)
		else:
			self.model = torch.hub.load('ultralytics/yolov5', 'custom', path = model_path)

	def run(self,img):
		try:
			outputs = self.model(img)
		except:
			return list()

		# convert to pandas
		res = outputs.pandas().xyxy[0]

		# filter out the result
		res = res[res['name'].isin(self.class_interest)]
		res = res[res['confidence']>=self.min_coonfidence]

		# convert to list 
		res['w'] = res['xmax'] - res['xmin']
		res['h'] = res['ymax'] - res['ymin']

		# convert to int
		res = res.astype({'xmin':int,'ymin':int,'w':int,'h':int})

		# format [xmin,ymin,w,h,score,class]
		labels = [[[x['xmin'],x['ymin'],x['w'],x['h']],x['confidence'],x['class']] for x in res.to_dict('records')]

		return labels