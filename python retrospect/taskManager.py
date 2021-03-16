# 服务进程

import random, time, queue
from multiprocessing.managers import BaseManager

# 第一步：建立task_queue和result_queue
task_queue = queue.Queue()
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass

def return_task_queue():
    return task_queue

def return_result_queue():
    return result_queue


if __name__ == '__main__':
# 第二步：把创建的两个队列暴露在网络上，callable参数关联了Queue对象
    QueueManager.register('get_task_queue', callable=return_task_queue)        # macOS下callable=lambda:task_queue不可用
    QueueManager.register('get_result_queue', callable=return_result_queue)


# 第三步：绑定端口8001，设置验证口令'qiye'。这个相当于对象的初始化
    manager = QueueManager(address=('127.0.0.1', 8001), authkey=b'qiye')


# 第四步：启动管理，监听信道
    manager.start()


# 第五步：通过管理实例的方法获得通过网络访问的Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()


# 第六步：添加任务
    for url in ['ImageUrl_'+str(i) for i in range(10)]:
        print('put task %s ...' % url)
        task.put(url)
    # 获取返回结果
    print('try get result...')
    for i in range(10):
        print('result is %s' % result.get(timeout=10))
# 关闭管理
    manager.shutdown()

