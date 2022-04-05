import os
import sys
import cv2
from tqdm import tqdm,trange
from dict2xml import dict2xml
from xml.dom.minidom import parseString

BASE_DIR = os.path.dirname(os.path.abspath('ALPR'))
sys.path.append(BASE_DIR)

from lib.model.ModelFactory import model_factory
from lib.utils.drawing import draw_bbox,draw_text,crop_img
from lib.dataloader.VideoDataloader import VideoLoader,VideoWriter


# Video Path
video_path = 'data/sample/ori.MOV'
output_path = 'data/sample/res.mp4'

# Set max frame
max_frame = 300

# =================================================================================================
model = dict()

#  Vehicle Model
model['vehicle'] = model_factory('YOLO')
model['vehicle'].load_model(model_path = os.path.join('weights','yolov5s.pt'))

#  LP Model
model['LP'] = model_factory('YOLO')
model['LP'].load_model(model_path = os.path.join('weights','LP_model.pt'))

model['LP'].class_names = ['license plate']
model['LP'].class_interest = ['license plate']
model['LP'].min_coonfidence = 0.05

# Tracking Model
model['tracking'] = model_factory('tracking')
model['tracking'].load_model()

# OCR Model
model['ocr'] = model_factory('ocr')
model['ocr'].load_model()

model['ocr'].min_coonfidence = 0.1

# =================================================================================================
# load video
imgs = VideoLoader(video_path,max_frame=max_frame)

# init writer
writer = VideoWriter(output_path)
writer.init_from_videoloader(imgs)

# ================================================================================================
xml = dict()
xml['Video Path'] = video_path
xml['Type'] = os.path.splitext(video_path)[-1]
xml['Width'] = imgs.width
xml['Height'] = imgs.height
xml['FrameRateMS'] = imgs.fps
xml['DurationMS'] = imgs.frames/imgs.fps
xml['frames'] = []

# ================================================================================================

# for every frame
for frame_id,img in enumerate(tqdm(imgs)):

	# Vehicle detection
	rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	result = model['vehicle'].run(rgb_img)
	result = model['tracking'].run(rgb_img,result)

	xml_frame = dict()
	xml_frame['delayMS'] = frame_id/imgs.fps
	xml_frame['ID'] = frame_id
	xml_frame['Vehicle'] = []

	# for every vehicle
	for bbox in result:

		xml_vehicle = dict()
		xml_vehicle['ID'] = str(bbox[-1])
		xml_vehicle['X'] = bbox[0][0]
		xml_vehicle['Y'] = bbox[0][1]
		xml_vehicle['Width'] = bbox[0][2]
		xml_vehicle['Height'] = bbox[0][3]
		xml_vehicle['LP'] = []

		# draw vehicle box and id
		img = draw_bbox(img,*bbox[0])
		img = draw_text(img,'id : '+str(bbox[-1]),*bbox[0])

		# LP detection
		cropped_vehicle = crop_img(rgb_img,*bbox[0])
		lp_result = model['LP'].run(cropped_vehicle)

		# for every LP
		for lp in lp_result:
			xml_LP = dict()

			# get the LP location in whole img
			lp[0][0] += bbox[0][0] # x
			lp[0][1] += bbox[0][1] # y

			# OCR
			cropped_lp = crop_img(rgb_img,*lp[0])
			ocr_result = model['ocr'].run(cropped_lp)

			# draw LP box
			img = draw_bbox(img,*lp[0],color=(0,0,255))

			# draw ocr text
			if len(ocr_result) > 0 :
				ocr_text,ocr_conf = ocr_result
				img = draw_text(img,str(ocr_text),*lp[0],color=(0,255,0),size=0.5,thickness=1)
				xml_LP['OCR'] = str(ocr_text)
				xml_LP['OcrProbability'] = str(ocr_conf)

			xml_LP['X'] = lp[0][0]
			xml_LP['Y'] = lp[0][1]
			xml_LP['Width'] = lp[0][2]
			xml_LP['Height'] = lp[0][3]

			xml_vehicle['LP'].append(xml_LP)

		xml_frame['Vehicle'].append(xml_vehicle)

	xml['frames'].append(xml_frame)
	writer.update(img)

xml = dict2xml(xml, wrap ='Video', indent ="\t")

xmlfile = open("ALPR_sample.xml", "w")
xmlfile.write(xml)
xmlfile.close()