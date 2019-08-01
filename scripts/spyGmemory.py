import pynvml
import threading
import time
from sendEmail import SendMail
import numpy as np

count = 0
# old_Mb = [99999] * 2
def seeGmemory(gpu_id):
    global count

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    Mb = meminfo.used / 1024 / 1024 ## B --> MB
    if Mb < 20000:
        SendMail(_subject = 'GPU free', _content = 'GPU free')
        return True
    else:
        count += 1
        print('spy {} times. memory = {} Mb'.format(count, Mb))
        return False


def seeGmemorys(gpu_ids, tag = None, limits = 10000):
    global count
    # global old_Mb
    Mb = []

    pynvml.nvmlInit()
    for gpu_id in gpu_ids:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        m = meminfo.used / 1024 / 1024
        Mb.append(m) ## B --> MB

    if limits is None:
        ## default: whether less than 10000 Mb
        status = np.array(list(map(lambda x: x < 10000, Mb)))
    else:
        ## optional: [lower, upper].
        ## lower < Memory < upper is good.
        assert isinstance(limits, list) and len(limits) == 2 and limits[0] < limits[1]
        status = np.array(list(map(lambda x: x < limits[0] or x > limits[1], Mb)))

    if status.any():
        SendMail(_subject = '{} stop'.format(tag), _content = 'GPU free')
        return True
    # elif (np.array(Mb) > np.array(old_Mb)).any():
    # 	SendMail(_subject = '{} increase'.format(tag), _content = 'GPU increase')
    # 	return False
    else:
        count += 1
        # old_Mb = Mb
        # print(['id = {}, memory = {} Mb'.format(i,m) for _,i,m in zip(enumerate(gpu_ids, Mb))])
        str = ', '.join(['id = {}, memory = {} Mb'.format(item[0], item[1]) for _,item in enumerate(zip(gpu_ids, Mb))])
        print('spy {} times. {}'.format(count, str))
        return False





def spy():
    while 1:
        # flag = seeGmemory(gpu_id = 3)
        flag = seeGmemorys(gpu_ids = [4,6], tag = 'xx')
        if flag:
            print('Over')
            break
        time.sleep(1) ## 1 seconds


if __name__ == '__main__':
    t = threading.Thread(target = spy)
    t.start()