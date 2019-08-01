import pynvml
import threading
import time
import numpy as np

from sendEmail import SendMail
from spyGmemory import seeGmemorys
from spyLog import seeLog





def spy():

    tag = 'xx'
    log_file = 'xx.log'

    while 1:
        flag1 = seeGmemorys(gpu_ids = [0,1], tag = tag, limits = [10000, 22900])
        flag2 = seeLog(log_file = log_file, tag = tag)

        if flag1 or flag2:
            print('Over')
            break
        time.sleep(1) ## seconds


if __name__ == '__main__':
    t = threading.Thread(target = spy)
    t.start()


