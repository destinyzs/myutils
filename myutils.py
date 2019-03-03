import os, sys
import numpy as np
import cv2


################################################## Boxes ##################################################

def transYxyx2Xyxy(boxes, with_label_last = False):
	'''
	Transform boxes' format from (y1,x1, y2,x2...(label)) to (x1,y1, x2,y2...(label))
	
	Arguments:
		boxes: ndarray, [N, (y1,x1, y2,x2...)]
	
	Returns:
		boxes: ndarray, [N, (x1,y1, x2,y2...)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	# ys = [boxes[:, i*2] for i in range(boxes.shape[1]//2)]
	# xs = [boxes[:, i*2+1] for i in range(boxes.shape[1]//2)]
	if with_label_last:
		tp = boxes[:,:-1]
	else:
		tp = boxes
	xs = tp[:, 0::2]
	ys = tp[:, 1::2]
	assert len(ys) == len(xs), 'xs and ys must have the same length.'

	result = []
	for i in range(len(ys)):
		result.append(xs[i])
		result.append(ys[i])
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyxy2Yxyx(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x1,y1, x2,y2...(label)) to (y1,x1, y2,x2...(label))
	
	Arguments:
		boxes: ndarray, [N, (x1,y1, x2,y2...)]
	
	Returns:
		boxes: ndarray, [N, (y1,x1, y2,x2...)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	# xs = [boxes[:, i*2] for i in range(boxes.shape[1]//2)]
	# ys = [boxes[:, i*2+1] for i in range(boxes.shape[1]//2)]
	if with_label_last:
		tp = boxes[:,:-1]
	else:
		tp = boxes
	xs = tp[:, 0::2]
	ys = tp[:, 1::2]
	assert len(ys) == len(xs), 'xs and ys must have the same length.'

	result = []
	for i in range(len(xs)):
		result.append(ys[i])
		result.append(xs[i])
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyxy2Xyxyxyxy(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x1,y1, x2,y2 (label)) to (x1,y1, x2,y2, x3,y3, x4,y4 (label))
	
	Arguments:
		boxes: ndarray, [N, (x1,y1, x2,y2)]
	
	Returns:
		boxes: ndarray, [N, (x1,y1, x2,y2, x3,y3, x4,y4)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	x1 = boxes[:, 0]
	y1 = boxes[:, 1]
	x2 = boxes[:, 2]
	y2 = boxes[:, 3]
	result = [x1, y1, 
			  x2, y1, 
			  x2, y2, 
			  x1, y2]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyxyxyxy2Xyxy(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x1,y1, x2,y1, x2,y2, x1,y2 (label)) to (x1,y1, x2,y2 (label))
	
	Arguments:
		boxes: ndarray, [N, (x1,y1, x2,y1, x2,y2, x1,y2)]
	
	Returns:
		boxes: ndarray, [N, (x1,y1, x2,y2)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	# xs = [boxes[:, i*2] for i in range(boxes.shape[1]//2)]
	# ys = [boxes[:, i*2+1] for i in range(boxes.shape[1]//2)]
	if with_label_last:
		tp = boxes[:,:-1]
	else:
		tp = boxes
	xs = tp[:, 0::2]
	ys = tp[:, 1::2]
	x1 = np.min(xs, axis = -1)
	y1 = np.min(ys, axis = -1)
	x2 = np.max(xs, axis = -1)
	y2 = np.max(ys, axis = -1)
	result = [x1, y1, x2, y2]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyxy2XyCtrWh(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x1,y1, x2,y2 (label)) to (x_ctr,y_ctr, w,h (label))
	
	Arguments:
		boxes: ndarray, [N, (x1,y1, x2,y2)]
	
	Returns:
		boxes: ndarray, [N, (x_ctr,y_ctr, w,h)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	x1 = boxes[:, 0]
	y1 = boxes[:, 1]
	x2 = boxes[:, 2]
	y2 = boxes[:, 3]

	x_ctr = (x1 + x2) * 0.5
	y_ctr = (y1 + y2) * 0.5
	w = x2 - x1
	h = y2 - y1
	result = [x_ctr, y_ctr, w, h]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyCtrWh2Xyxy(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x_ctr,y_ctr, w,h (label)) to (x1,y1, x2,y2 (label))
	
	Arguments:
		boxes: ndarray, [N, (x_ctr,y_ctr, w,h)]
	
	Returns:
		boxes: ndarray, [N, (x1,y1, x2,y2)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	x_ctr = boxes[:, 0]
	y_ctr = boxes[:, 1]
	w = boxes[:, 2]
	h = boxes[:, 3]

	x1 = x_ctr - w * 0.5
	y1 = y_ctr - h * 0.5
	x2 = x_ctr + w * 0.5
	y2 = y_ctr + h * 0.5
	result = [x1, y1, x2, y2]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)

def transXyCtrWh2Xyxyxyxy(boxes, with_label_last = False):
	'''
	Transform boxes' format from (x_ctr,y_ctr, w,h (label)) to (x1,y1, x2,y1, x2,y2, x1,y2 (label))
	
	Arguments:
		boxes: ndarray, [N, (x_ctr,y_ctr, w,h)]
	
	Returns:
		boxes: ndarray, [N, (x1,y1, x2,y1, x2,y2, x1,y2)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	x_ctr = boxes[:, 0]
	y_ctr = boxes[:, 1]
	w = boxes[:, 2]
	h = boxes[:, 3]

	x1 = x_ctr - w * 0.5
	y1 = y_ctr - h * 0.5
	x2 = x_ctr + w * 0.5
	y2 = y_ctr + h * 0.5
	result = [x1, y1, 
			  x2, y1, 
			  x2, y2, 
			  x1, y2]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)


def rescale_WhOfBoxes_ByRatio(boxes, ratio, with_label_last = False):
	'''
	Rescale boxes' width and height by ratio(w,h), in the case where the center doesn't change
	
	Arguments:
		boxes: ndarray, [N, (x_ctr,y_ctr, w,h)]
		ratio: int or tuple(w,h)
	
	Returns:
		boxes: ndarray, [N, (x_ctr,y_ctr, w,h)]
	'''
	if not with_label_last:
		assert boxes.shape[1] % 2 == 0, 'boxes format error.'
	x_ctr = boxes[:, 0]
	y_ctr = boxes[:, 1]
	w = boxes[:, 2]
	h = boxes[:, 3]

	assert type(ratio) in [int, tuple], 'Unknown ratio type.'
	if type(ratio) == int:
		w, h = w * ratio, h * ratio
	if type(ratio) == tuple:
		w, h = w * ratio[0], h * ratio[1]

	result = [x_ctr, y_ctr, w, h]
	if with_label_last:
		label = boxes[:, -1]

	if with_label_last:
		return np.stack(result + [label], axis = 1).astype(boxes.dtype)
	else:
		return np.stack(result, axis = 1).astype(boxes.dtype)


def transQuadrangle2Rotate(coordinates):
	"""
	Transform boxes from (x1,y1, x2,y2, x3,y3, x4,y4) to (x_ctr, y_ctr, w, h, theta), -90<=theta<0

	Arguments:
		coordinates: ndarray, [N, (x1,y1, x2,y2, x3,y3, x4,y4)] 

	Returns:
		coordinates: ndarray, [N, (x_ctr, y_ctr, w, h, theta)] 
	"""
	assert coordinates.shape[1] % 2 == 0, 'boxes format error.'
	result = []
	for cd in coordinates:
		cd = np.int0(cd)
		cd = cd.reshape([4, 2])
		poly = cv2.minAreaRect(cd) ## ((x,y), (w,h), theta)

		x, y, w, h, theta = poly[0][0], poly[0][1], poly[1][0], poly[1][1], poly[2]
		result.append([x, y, w, h, theta])

	return np.array(result, dtype = np.float32)

def transRotate2Quadrangle(coordinates):
	"""
	Transform boxes from (x_ctr, y_ctr, w, h, theta) to (x1,y1, x2,y2, x3,y3, x4,y4).

	Arguments:
		coordinates: ndarray, [N, (x_ctr, y_ctr, w, h, theta)] 

	Returns:
		coordinates: ndarray, [N, (x1,y1, x2,y2, x3,y3, x4,y4)] 
	"""
	result = []
	for cd in coordinates:
		quad = cv2.boxPoints(((cd[0], cd[1]), (cd[2], cd[3]), cd[4]))
		result.append(np.reshape(quad, [-1, ]))

	return np.array(result, dtype = np.float32)

def get_horizen_minAreaRectangle_by_rotate_box(coordinates):
	"""
	Get the minimum horizontal rectangle from rotate box.
		From (x_ctr, y_ctr, w, h, theta) to (x1,y1, x2,y2).

	Arguments:
		coordinates: ndarray, [N, (x_ctr, y_ctr, w, h, theta)] 

	Returns:
		coordinates: ndarray, [N, (x1,y1, x2,y2)] 
	"""
	## 1. Convert (x_ctr, y_ctr, w, h, theta) to (x1, y1, x2, y2, x3, y3, x4, y4)
	boxes_convert = transRotate2Quadrangle(coordinates = coordinates)
	## 2. Convert to (x1, y1, x2, y2)
	xs = boxes_convert[:, 0::2]
	ys = boxes_convert[:, 1::2]
	x1 = np.min(xs, axis = -1)
	y1 = np.min(ys, axis = -1)
	x2 = np.max(xs, axis = -1)
	y2 = np.max(ys, axis = -1)
	result = [x1, y1, x2, y2]

	return np.stack(result, axis = 1).astype(np.float32)



################################################## OS ##################################################
import os


def get_base_name(p):
	'''
	Return the splitext name.
		e.g. 'qwe/rty/uio.png' --> 'uio'
	'''
	return os.path.splitext(os.path.basename(p))[0]

def check_dir(p):
	if not os.path.exists(p):
		os.makedirs(p)