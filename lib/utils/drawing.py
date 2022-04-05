import cv2

def draw_bbox(img,x1,y1,w,h,color=(255,0,0)):
	x2 = x1+w
	y2 = y1+h
	img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

	return img

def draw_text(img,text,x1,y1,w,h,color=(0,0,255),size=1,thickness=2):
	img = cv2.putText(img,text,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,size,color,2)

	return img

def crop_img(source,x,y,w,h):
	img = source.copy()
	im_h,im_w,_ = img.shape

	if x<0 :
		x = 0
	if y<0 :
		y = 0
	if w<0:
		w = 0
	if h<0 :
		h = 0

	if x >= im_w:
		x = im_w - 1
	if y >= im_h:
		y = im_h - 1

	crop_img = img[y:y+h, x:x+w]
	
	return crop_img
 
def less_tight_box(x,y,w,h,ratio = 0.5):
	x_factor = w*ratio
	y_factor = h*ratio

	x = int(x - x_factor/2)
	y = int(y - y_factor/2)

	w = int(w + x_factor)
	h = int(h + y_factor)

	return x,y,w,h