import cv2
import sys
import os
import json
import torch
import time 
import pandas as pd

from datetime import datetime
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath('ALPR'))
sys.path.append(BASE_DIR)

from deep_sort_realtime.deepsort_tracker import DeepSort
from lib.drawing import draw_bbox

# ========================================== CONFIG ========================================== 
# Video Path
video_path = 'data/sample/sample_1.mp4'

# Set max frame
max_frame = 300

# load the detection model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  

# load the tracking model
tracker = DeepSort(max_age=30, nn_budget=70, override_track_class=None)

# ========================================== END OF CONFIG ==========================================

# prepare video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('data/output.mp4', fourcc, 30, (1280, 720))

# load video
vidcap = cv2.VideoCapture(video_path)
success,img = vidcap.read()

st = time.time()
idx = 0
while success and idx <= max_frame:
	print('Reading frame',idx)
	success,img = vidcap.read()
	# load img
	img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	# inference
	results = model(img_rgb)
	res = results.pandas().xyxy[0]
	res = res[res['class']==2]
	res = res[res['confidence']>=0.5]

	res['w'] = res['xmax'] - res['xmin']
	res['h'] = res['ymax'] - res['ymin']

	# tracking
	labels = [([x['xmin'],x['ymin'],x['w'],x['h']],x['confidence'],x['class']) for x in res.to_dict('records')]
	tracks = tracker.update_tracks(labels, frame=img)

	# Draw detcetion
	for track in tracks:
		x1,y1,x2,y2 = list(map(int, track.to_ltrb()))
		img = draw_bbox(img,x1,y1,x2,y2)
		obj_id = 'id : '+str(track.track_id)

		img = cv2.putText(img,obj_id,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
		video.write(img)

	idx+=1

print(time.time() -st)
video.release()