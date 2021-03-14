# 使用multiprocessing模块的Pool类来代表进程池对象
# Pool默认大小是CPU的核数，当有新的请求提交到Pool时如果池还没有满就会创建一个新的进程来执行该请求
from multiprocessing import Pool
import os, time, random


def run_task(name):
    print('Task %s (pid = %s) is running...' % (name, os.getpid()))
    time.sleep(random.random() * 3)
    print('Task %s end.' % name)


if __name__ == '__main__':
    print('Current process %s.' % os.getpid())
    p = Pool(processes=3)               # 容量为3的进程池，一次性最多运行3个
    for i in range(5):                  # 创建5个进程
        p.apply_async(run_task, args=(i, ))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
'''
Current process 69181.
Waiting for all subprocesses done...
Task 0 (pid = 69183) is running...
Task 1 (pid = 69184) is running...
Task 2 (pid = 69185) is running...
Task 1 end.
Task 3 (pid = 69184) is running...
Task 3 end.
Task 4 (pid = 69184) is running...
Task 2 end.
Task 0 end.
Task 4 end.
All subprocesses done.

根据输出也能看出一开始只运行3个并且后来运行的pid与刚刚结束的pid相同
'''