# gevent提供pool对象, 在处理大量网络和IO操作时是非常需要的
# 当池满时就是让后来的协程等待
from gevent import monkey
monkey.patch_all()
from urllib import request as urllib2
from gevent.pool import Pool


def run_task(url):
    print('Visit ---> %s' % url)
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        print('%d bytes received from %s.' % (len(data), url))
    except Exception as e:
        print(e)
    return 'url:%s ---> finish' % url


if __name__ == '__main__':
    # 池大小为2
    pool = Pool(2)
    urls = ['https://github.com/', 'https://www.python.org/', 'http://www.cnblogs.com/']
    results = pool.map(run_task, urls)
    print(results)
# 运行结果显示确实是先运行了前两个url，等待一个退出后再运行第三个
