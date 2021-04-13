'''
    第一个项目中采用了set内存去重的方式，如果直接存储大量的URL链接特别是URL较长时，容易造成内存溢出，

    --->所以我们将爬取的URL进行MD5处理，字符串经MD5处理后的信息摘要长度为128位，将生成的MD5摘要存储到set后，
    可以减少好几倍的内存消耗，python中的MD5算法生成的是32位字符串，由于我们爬取的URL较少，MD5冲突不大，
    完全可以取中间的16位字符串，即16位MD5加密。MD5加密指一种单向加密，将字符串转化成128bit的大整数。

    --->我们同时添加save_progress和load_progress方法进行序列化的操作，将未爬取的URL和已爬取的URL存在本地，
    保存当前进度，以便下次恢复状态
'''
import _pickle  # python2中的cPickle改名为py3中的_pickle
import hashlib


class UrlManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt')  # 未爬取的URL集合
        self.old_urls = self.load_progress('old_urls.txt')  # 已爬取的URL集合

    def has_new_url(self):
        '''
        判断是否有未爬取的url
        :return:
        '''
        return self.new_urls_size() != 0

    def get_new_url(self):
        '''
        获取未爬取的url
        :return:
        '''
        new_url = self.new_urls.pop()
        # MD5加密
        m = hashlib.md5()
        m.update(new_url.encode('utf-8'))       # 要先编码才能后hash
        self.old_urls.add(m.hexdigest()[8:-8])  # 共32位取中间的16位
        return new_url

    def add_new_url(self, url):
        '''
        将新的URL添加到未爬取的URL集合中
        :return:单个url
        '''
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode('utf-8'))       # 先编码后hash
        url_md5 = m.hexdigest()[8:-8]
        # 只对已爬取的URL集合进行MD5操作，毕竟只起到判断是否存在的条件，并不会拿old_urls的内容使用, 占用内存越少越好
        if url_md5 not in self.old_urls and url not in self.new_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        将新的URL添加到未爬取集合中
        :param urls: 新的url集合
        :return:
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_urls_size(self):
        return len(self.new_urls)

    def old_urls_size(self):
        return len(self.old_urls)

    def save_progress(self, path, data):
        '''
        保存进度
        :param path:文件路径
        :param data: 数据
        :return:
        '''
        with open(path, 'wb') as f:
            _pickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地加载进度
        :param path:文件路径
        :return:
        '''
        print('[+] 从文件加载进度: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = _pickle.load(f)
                return tmp
        except:
            print('[!] 无进度文件，创建: %s' % path)
        return set()
