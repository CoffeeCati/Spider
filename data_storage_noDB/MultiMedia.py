'''
    如果只需要文件的URL那么JSON和CSV存储已经够用，但是如果想要下载下来媒体文件，则需要urllib库支持urlretrieve()函数
    urlretrieve(url, filename=None, reporthook=None, data=None)
    filename: 指定本地存储路径，若未指定，urllib会生成一个临时文件
    reporthook: 是一个回调函数，可以利用其显示当前的下载进度
    data: 指post到服务器的数据，该方法返回一个元组(filename, headers)分别表示保存到本地的路径、服务器的响应头
'''
import urllib, requests
from lxml import etree
def Schedule(blocknum, blocksize, totalsize):
    '''
    :param blocknum: 已经下载的数据块
    :param blocksize: 数据块的大小
    :param totalsize: 远程文件的大小
    :return:
    '''
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print('当前下载进度%d' % per)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0)'
headers = {'User-Agent': user_agent}
url = 'http://www.ivsky.com/tupian/ziranfengguang/'
r = requests.get(url, headers=headers)
# 使用lxml解析网页
html = etree.HTML(r.text)
img_urls = html.xpath('.//img/src')     # 找到所有的img
i = 0
for img_url in img_urls:
    urllib.urlretrieve(img_url, 'img'+str(i)+'.jpg', Schedule)
    i += 1