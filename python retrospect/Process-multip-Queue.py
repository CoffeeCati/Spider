''' 使用Queue实现进程间的通信
1. Put方法: 插入数据到队列中，有两个可选参数blocked，timeout
当blocked = True(默认值) 时阻塞 timeout > 0 时间后队列仍为满状态，则抛出Queue.Full异常
当blocked = False 时，如果队列为满则立刻抛出Queue.Full异常
2. Get方法可以从队列获取并删除一个元素，有两个可选出参数blocked，timeout
当blocked = True(默认值) 时在 timeout > 0 时间内没有取到任何值则抛出Queue.Empty异常
当blocked = False 时，如果Queue有一个值可用则立即返回该值；如果队列为空则立即抛出Queue.Empty异常
'''
from multiprocessing import Process, Queue
import os, time, random


# 写数据
def proc_write(q, urls):
    print('Process(%s) is writing...' % os.getpid())
    for url in urls:
        q.put(url)
        print('Put %s to queue...' % url)
        time.sleep(random.random())


# 读数据
def proc_read(q):
    print('Process(%s) is reading...' % os.getpid())
    while True:
        url = q.get(True)
        print('Get %s from queue...' % url)


if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    proc_write1 = Process(target=proc_write, args=(q, ['url_1', 'url_2', 'url_3']))
    proc_write2 = Process(target=proc_write, args=(q, ['url_4', 'url_5', 'url_6']))
    proc_reader = Process(target=proc_read, args=(q,))
    # 启动子进程，写入
    proc_write1.start()
    proc_write2.start()
    # 启动子进程，读取
    proc_reader.start()
    # 等待proc_write结束
    proc_write1.join()
    proc_write2.join()
    # 由于proc_reader中while语句时死循环，因此要手动终止
    proc_reader.terminate()

