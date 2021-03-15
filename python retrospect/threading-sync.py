# Thread对象的Lock和RLock可以实现简单的线程同步，两个对象都有acquire方法和release方法，对应PV操作
'''
Lock:
如果一个线程acquire两次，由于第一次acquire没有release，第二次acquire会导致该线程被挂起，引发死锁
RLock:
一个线程可以多次acquire，因为内部使用counter维护线程acquire的次数，必须满足一个acquire对应一个release
当所有的release操作完成后别的线程才能申请该RLock对象
'''
import threading, time, random
mylock = threading.RLock()
num = 0


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        global num
        while True:
            mylock.acquire()
            print('%s locked, Number: %d' % (threading.current_thread().name, num))
            time.sleep(random.random())
            if num >= 4:
                mylock.release()
                print('%s released, Number: %d' % (threading.current_thread().name, num))
                break
            num += 1
            print('%s released, Number: %d' % (threading.current_thread().name, num))
            mylock.release()


# 让thread2在thread1结束后再运行，实现同步
if __name__ == '__main__':
    thread1 = MyThread('Thread_1')
    thread2 = MyThread('Thread_2')
    thread1.start()
    thread2.start()

# 程序运行结果与开头描述一致
