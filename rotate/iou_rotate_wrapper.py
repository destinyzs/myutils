import numpy as np
import torch
import cv2

from .rbbox_overlaps import rbbx_overlaps
from .iou_cpu import get_iou_matrix


def iou_rotate(boxes1, boxes2):
	'''
	GPU or CPU rotate IOU.
	
	Arguments:
		boxes1: [N1, 5(x_ctr, y_ctr, w, h, theta(angle))]
		boxes2: [N2, 5(x_ctr, y_ctr, w, h, theta(angle))]

	Returns:
		IoU: [N1, N2]
	'''
	if isinstance(boxes1, torch.Tensor) and isinstance(boxes2, torch.Tensor):
		is_tensor = True
		if boxes1.is_cuda:
			device_id = boxes1.get_device()
		boxes1_np = boxes1.detach().cpu().numpy()
		boxes2_np = boxes2.detach().cpu().numpy()
	elif isinstance(boxes1, np.ndarray) and isinstance(boxes2, np.ndarray):
		is_tensor = False
		boxes1_np = boxes1
		boxes2_np = boxes2
	else:
		raise TypeError(
			'boxes1 and boxes2 must have the same type, but got {} for boxes1 and {} for boxes2'.format(
				type(boxes1), type(boxes2)))

	iou_matrix = (rbbx_overlaps(boxes1_np, boxes2_np, device_id = device_id)
					if device_id is not None else get_iou_matrix(boxes1_np, boxes2_np))

	if is_tensor:
		iou_matrix = boxes1.new_tensor(iou_matrix, dtype = torch.float)
	else:
		iou_matrix = np.array(iou_matrix, dtype = np.float32)
	return iou_matrix
