from .YOLO.YOLO import YOLO 
from .DeepSORT.DeepSORT import DeepSORT
from .OCR.CRNN import CRNN

def _get_ocr_model():
	model = CRNN()
	return model

def _get_yolo_model():
	model = YOLO()
	return model

def _get_tracking_model():
	model = DeepSORT()
	return model

def model_factory(key):
	if key == 'YOLO':
		return _get_yolo_model()
	elif key == 'tracking':
		return _get_tracking_model()
	elif key == 'ocr':
		return _get_ocr_model()
	else:
		assert '{} model not found'.format(key)
