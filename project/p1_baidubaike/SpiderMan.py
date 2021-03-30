# 爬虫调度器来协调管理其他模块进行工作, 通过crawl(root_url)方法传入入口url
# 抓取100个百度百科标题、摘要、涉及到的关键词URL
from URLManager import UrlManager
from DataStorager import DataOutput
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口url
        self.manager.add_new_url(root_url)
        # 判断管理器中是否有新的url，同时判断抓取了多少个url
        while self.manager.has_new_url() and len(self.manager.old_urls) < 100:
            try:
                # 从URL管理器中获取新的url
                new_url = self.manager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页关键词URL和标题摘要data
                new_urls, data = self.parser.parser(new_url, html)
                # 将抽取的url放入URL管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器存储文件
                self.output.store_data(data)
                print('已经抓取%s个链接' % self.manager.old_url_size())
            except Exception:
                print('crawl failed')
        self.output.output_html('baike.html')


if __name__ == '__main__':
    url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB'
    spider_man = SpiderMan()
    spider_man.crawl(url)





