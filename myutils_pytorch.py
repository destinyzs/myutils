import torch
import torch.nn as nn



def GlobalAvgPooling2d(x):
	'''Global Average Pooling 2D
	
	Arguments:
		x: [B, C, H, W]
	'''

	return nn.AvgPool2d(kernel_size = x.size()[2:])(x).view(x.size()[:2])


def Reduce_Sum(x):
	'''Sum up all in x(list) in PyTorch.
	
	Arguments:
		x: list, each has the same shape
	'''
	assert type(x) == list, 'Only List Support!'
	if len(x) == 1:
		return x

	re = x[0]
	for xx in x[1:]:
		re += xx
	return re