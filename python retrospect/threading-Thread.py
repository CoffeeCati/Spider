# 从threading.Thread继承创建线程类
import random
import threading
import time


# 继承父类threading.Thread
class MyThread(threading.Thread):
    # 构造方法，在该类实例化时会自动调用，此处覆盖了父类的__init__
    def __init__(self, name, urls):
        # 子类重写但还需要调用被覆盖的父类__init__时
        threading.Thread.__init__(self, name=name)  # 等价于 super(MyThread, self).__init__(name=name)
        self.urls = urls

    def run(self):
        print('Current %s is running...' % threading.current_thread().name)
        for url in self.urls:
            print('%s --->>> %s' % (threading.current_thread().name, url))
            time.sleep(random.random())
        print('%s ended.' % threading.current_thread().name)


print('%s is running...' % threading.current_thread().name)
t1 = MyThread(name='Thread_1', urls=['url_1', 'url_2', 'url_3'])
t2 = MyThread(name='Thread_2', urls=['url_4', 'url_5', 'url_6'])
t1.start()
t2.start()
t1.join()
t2.join()
print('%s ended.' % threading.current_thread().name)
