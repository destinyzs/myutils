# import pynvml
import threading
import time
from sendEmail import SendMail


count = 0
log_len = 0
interval = 1 ## seconds

def seeLog(log_file, tag):
    global count
    global log_len

    with open(log_file, 'rb') as f:
        lines = f.readlines()

    l_len = len(lines)
    if l_len != log_len:
        log_len = l_len
        count = 0
    else:
        count += 1

    if count * interval > 20*60:
        ## if file did't change in count seconds, 
        ## send email. 
        SendMail(_subject = '{} Process Stop!!!'.format(tag), _content = '{} Process Stop!!!'.format(tag))
        return True
    else:
        print('file length = {}, sustain {} seconds/{:4f} minutes.'.format(log_len, count*interval, count*interval / 60.))
        return False




def spy():
    log_file = 'xx.log'
    while 1:
        flag = seeLog(log_file = log_file, tag = 'xx')
        if flag:
            print('Over')
            break
        time.sleep(interval) ## seconds


if __name__ == '__main__':
    t = threading.Thread(target = spy)
    t.start()	
