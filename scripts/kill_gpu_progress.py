import os,sys
import pynvml

def clear_gpu(gpu_ids):
    pynvml.nvmlInit()
    for gpu_id in gpu_ids:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        pros = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        for pro in pros:
            print('find Pid {} on GPU {}.'.format(pro.pid, gpu_id))
            os.system('sudo kill -9 {}'.format(pro.pid))


if __name__ == '__main__':

    ## python kill_gpu_progress.py 0
    ## python kill_gpu_progress.py 0,1,2,3
    gpus = sys.argv
    if len(gpus) == 1:
        raise ValueError
    gpus = list(map(int, gpus[1].split(',')))

    clear_gpu(gpu_ids = gpus)
    print('clear.')