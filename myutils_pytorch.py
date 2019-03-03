import torch
import torch.nn as nn



def GlobalAvgPooling2d(x):
	'''Global Average Pooling 2D
	
	Arguments:
		x: [B, C, H, W]
	'''

	return nn.AvgPool2d(kernel_size = x.size()[2:])(x).view(x.size()[:2])

########## Updated By LCZ, time: 2019.1.16 ##########
########## Updated By LCZ, time: 2019.1.18, fix bug. ##########
def Reduce_Sum(x):
	'''Sum up all in x(list).

	Arguments:
		x: list, each has the same shape
	'''
	assert type(x) == list or type(x) == tuple, 'Only List and Tuple Support!'
	if len(x) == 1:
		return x[0]

	re = torch.zeros_like(x[0], dtype=x[0].dtype)
	for xx in x[:]:
		re += xx

	return re


########## Updated By LCZ, time: 2019.2.27 ##########
def one_hot(inp, depth, on_value = None, off_value = None, dtype = None):
	'''
	Convert tensor into one-hot encode.
	
	Arguments:
		inp: int, tensor
		depth: int
		on_value, off_value: optional, the location represented by inp take value on_value, 
										while all other locations take value off_value.
		dtype: optional, output dtype.
	
	Returns:
		tensor
	'''
	valid_tp = [torch.uint8, torch.int, torch.int8, torch.int16, torch.int32, torch.int64]
	assert inp.dtype in valid_tp,\
			'Only support [' + ','.join([tp.__str__() for tp in valid_tp]) + '], but get {}'.format(inp.dtype)
	inp_ex = inp.type(torch.LongTensor).unsqueeze(dim = -1)
	one_hot = torch.zeros(inp.shape + (depth,)).scatter_(-1, inp_ex, 1)
	if on_value is not None:
		one_hot[one_hot==1] = on_value
	if off_value is not None:
		one_hot[one_hot==0] = off_value
	if dtype is not None:
		one_hot = one_hot.type(dtype)
	return one_hot