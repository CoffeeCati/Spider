# 协程——微线程，协程调度切换时会保留上一次调用时的状态，协程需要用户自己写调度程序，不需要CPU参与
# python通过yield提供了对协程的基本支持，但是gevent提供了完善的协程支持。
# gevent自动切换协程，而不会等待IO，所以gevent要修改python标准库，将一些常见的阻塞，如select, socket等地方实现协程跳转
# 通过monkey patch实现
from gevent import monkey; monkey.patch_all()
import gevent
from urllib import request as urllib2    # python3中把urllib2合并进urllib.request


def run_task(url):
    print('Visit ---> %s' % url)
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        print('%d bytes received from %s.' % (len(data), url))
    # 捕获所有异常
    except Exception as e:
        print(e)


if __name__ == '__main__':
    urls = ['https://github.com/', 'https://www.python.org/', 'http://www.cnblogs.com/']
    greenlets = [gevent.spawn(run_task, url) for url in urls]
    gevent.joinall(greenlets)

