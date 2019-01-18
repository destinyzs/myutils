import torch
import torch.nn as nn



def GlobalAvgPooling2d(x):
	'''Global Average Pooling 2D
	
	Arguments:
		x: [B, C, H, W]
	'''

	return nn.AvgPool2d(kernel_size = x.size()[2:])(x).view(x.size()[:2])


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