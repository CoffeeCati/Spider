'''
    控制调度器
    主要产生并启动URL管理进程、数据提取进程、数据存储进程，同时维护4个队列保持进程间的通信，分别为
    url_queue、result_queue、conn_q、store_q
    url_q: 是URL管理进程将URL传递给爬虫节点的通道
    result_q: 是爬虫节点将数据返回给数据提取进程的通道
    conn_q: 是数据提取进程将新的URL数据交给URL管理进程的通道
    store_q: 是数据提取进程将获取的数据交给数据存储进程的通道

    python retrospect/taskManger.py
'''
from URLManager import UrlManager
from DataOutput import DataOutput
import multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import Process
import queue, time


# 控制节点
class NodeManager(BaseManager):
    def start_Manger(self, url_q, result_q):
        '''
        创建一个分布式管理器
        :param url_q: url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列在网络上，利用register方法，callable参数关联了Queue对象
        # 不能在__main__中使用lambda，在对象中却可以，具体原因不明
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'baike')
        return manager

    # url管理进程, 将从conn_q队列获取到新的URL提交给URL管理器，去重后取出URL放入url_q队列传给爬虫节点
    def url_manager_proc(self, url_q, conn_q, root_url):
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while url_manager.has_new_url():
                # 从URL管理器获取新的URL
                new_url = url_manager.get_new_url()
                # 将新的URL发给工作节点
                url_q.put(new_url)
                print('old_url =', url_manager.old_urls_size())
                # 加一个判断条件，当爬取100个链接后就关闭，并保存进度
                if url_manager.old_urls_size() > 100:
                    # 通知爬虫节点工作关闭
                    url_q.put('end')
                    print('控制节点发起关闭通知')
                    # 关闭管理节点，同时存储set状态
                    url_manager.save_progress('new_urls.txt', url_manager.new_urls)
                    url_manager.save_progress('old_urls.txt', url_manager.old_urls)
                    return
                # 将从result_solve_proc获得的URL添加到URL管理器
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException:
                time.sleep(0.1) # 延时休息

    # 数据提取进程, 从result_q队列读取返回的数据，并将数据中的URL添加到conn_q队列交给URL管理进程，将数据添加到store_q交给数据存储进程
    def result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get()
                    if content['new_urls'] == 'end':
                        # 如果得到结束通知则结束
                        print('数据提取进程接收通知然后结束！')
                        store_q.put('end')
                        return
                    conn_q.put(content['new_urls'])     # url为set类型
                    store_q.put(content['data'])       # 解析出来的数据为dict类型
                else:
                    time.sleep(0.1)
            except BaseException:
                time.sleep(0.1)

    # 数据存储进程, 从store_q获取数据，并调用数据存储器进行数据存储
    def store_proc(self, store_q: queue.Queue):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('数据存储进程接收通知然后结束!')
                    output.output_end()
                    return
                output.store_data(data)
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    # 初始化4个队列
    url_q = multiprocessing.Queue()     # ！！！在多线程模式下使用queue.Queue()，在多进程模式下使用multiprocessing.Queue()
    result_q = multiprocessing.Queue()  # 一开始我使用了queue.Queue()会报错，因为线程锁导致序列化失败
    conn_q = multiprocessing.Queue()
    store_q = multiprocessing.Queue()
    # 创建分布式管理器
    node = NodeManager()
    manager = node.start_Manger(url_q, result_q)
    # 创建url管理进程、数据提取进程、数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc, args=(url_q, conn_q, 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB',))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()


