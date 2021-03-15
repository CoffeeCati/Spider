'''Pipe通信机制
1. Pipe方法返回(conn1, conn2)代表管道两端，两个通信的进程分别位于管道两端
2. send方法和recv方法分别为发送消息和接收消息
3. Pipe方法有duplex参数，当duplex = True(默认值) 时为全双工即conn1和conn2均可收发；
当duplex = False 时conn1只能接收，conn2只能发送。当没有消息可以接收时，recv方法会一直阻塞，
如果管道已经关闭，那么recv方法会抛出EOFError
'''
import multiprocessing
import random
import time, os


def proc_send(pipe, urls):
    for url in urls:
        print('Process(%s) send: %s' % (os.getpid(), url))
        pipe.send(url)
        time.sleep(random.random())


def proc_recv(pipe):
    while True:
        print('Process(%s) receive:%s' % (os.getpid(), pipe.recv()))
        time.sleep(random.random())


if __name__ == '__main__':
    # 分配Pipe给父进程
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc_send, args=(pipe[0], ['url_'+str(i) for i in range(10)]))
    p2 = multiprocessing.Process(target=proc_recv, args=(pipe[1], ))
    # 启动子进程，发送
    p1.start()
    # 启动子进程，接收
    p2.start()
    # 等待发送进程结束
    p1.join()
    # 手动终止接收进程，因为while为死循环
    p2.terminate()
