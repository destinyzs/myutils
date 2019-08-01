import pynvml
import threading
import time
import numpy as np
import subprocess
from sendEmail import SendMail


count = 0
old_Mb = [99999] * 2
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


def seeGmemorys(gpu_ids, tag = None):
    global count
    global old_Mb
    Mb = []

    pynvml.nvmlInit()
    for gpu_id in gpu_ids:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
        m = meminfo.used / 1024 / 1024
        Mb.append(m) ## B --> MB
    if (np.array(Mb) < 10000).any():
        SendMail(_subject = '{} stop'.format(tag), _content = 'GPU free')
        return True
    # elif (np.array(Mb) > np.array(old_Mb)).any():
    # 	SendMail(_subject = '{} increase'.format(tag), _content = 'GPU increase')
    # 	return False
    else:
        count += 1
        old_Mb = Mb
        str = ', '.join(['id = {}, memory = {} Mb'.format(item[0], item[1]) for _,item in enumerate(zip(gpu_ids, Mb))])
        print('spy {} times. {}'.format(count, str))
        return False



def spy():
    while 1:
        # flag = seeGmemory(gpu_id = 2)
        flag = seeGmemorys(gpu_ids = [0,1,2,3], tag = 'xx')
        if flag:
            print('Over')
            time.sleep(5)
            break
        time.sleep(1) ## 1 seconds
    time.sleep(1) ## 1 seconds
    try:
        cmd = 'CUDA_VISIBLE_DEVICES=0,1,2,3 python xx'
        docker_names = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
        print('*'*100)

        flag = seeGmemorys(gpu_ids = [0,1,2,3], tag = 'xx')
    except(RuntimeError, KeyboardInterrupt, AssertionError, BrokenPipeError):
        SendMail(_subject = 'stop !', _content = 'stop !')




if __name__ == '__main__':
    t = threading.Thread(target = spy)
    t.start()