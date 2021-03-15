'''多线程优点
1. 运行时间长的任务可以放到后台运行
2. 用户界面可以更加吸引人，可以显示一个进度条来显示处理的进度
3. 程序运行速度快
4. 可以释放一些珍贵的资源，如内存
'''
# thread是低级模块，threading对thread进行了封装，绝大情况下只使用threading模块即可
# threading模块一般通过两种方式创建多线程:
# 1. 把函数传入并创建Thread实例，然后调用start方法
# 2. 直接从threading.Thread继承并创建线程类，然后重写__init__方法和run方法
import random
import time, threading, os

def thread_run(urls):
    print('Current %s is running...' % threading.current_thread().name)
    for url in urls:
        print('%s ---->>> %s Processid: %s' % (threading.current_thread().name, url, os.getpid()))
        time.sleep(random.random())
    print('%s ended.' % threading.currentThread().name)


print('%s(%s) is running...' % (threading.current_thread().name, os.getpid()))
t1 = threading.Thread(target=thread_run, name='Thread_1', args=(['url_'+str(i) for i in range(1, 4)],))
t2 = threading.Thread(target=thread_run, name='Thread_2', args=(['url_'+str(i) for i in range(4, 7)],))
t1.start()
t2.start()
t1.join()
t2.join()
print('%s ended.' % threading.current_thread().name)
