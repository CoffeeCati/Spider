# HTML解析器, 使用bs4解析, 提取相关词条页面的URL和当前词条的标题和摘要信息，首先要自己分析html结构找到对应的标记
# 标题位于<dd class="lemmaWgt-lemmaTitle-title"><h1></h1>下
# 摘要位于<div class="lemma-summary" label-module="lemmaSummary"><div class="para" label-module="para">内容</div></div>下
# 相关词条的href存放在<a target='_blank' href='/item/XXXXXXXX'>中
'''
python3版本中已经将urllib2、urlparse、和robotparser并入了urllib模块中，并且修改urllib模块，其中包含5个子模块，
即是help()中看到的那五个名字error, parse, request(urllib2), response, robotparser此处使用parser
'''
import re
from bs4 import BeautifulSoup
from urllib import parse


class HtmlParser(object):
    def parser(self, page_url, html_content):
        '''
        用于解析网页内容，抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_content: 该网页的html代码
        :return: 返回URL和数据
        '''
        if page_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        new_urls = self.__get_new_urls(page_url, soup)
        new_data = self.__get_new_data(page_url, soup)
        return new_urls, new_data

    def __get_new_urls(self, page_url, soup):
        '''
        抽取URL集合
        :param page_url:要抽取的页面的URL
        :param soup: 解析后的soup对象
        :return: 返回页面中的URL集合
        '''
        new_urls = set()
        # 抽取符合要求的<a>标记
        links = soup.find_all('a', target='_blank', href=re.compile(r'/item/.*'))   # 此处匹配到的是使用了类似xpath的相对路径
        for link in links:
            # 提取href属性
            new_url = link.get('href')
            # 拼接成完整的url
            new_full_url = parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def __get_new_data(self, page_url, soup):
        '''
        抽取有效数据
        :param page_url:下载页面的url
        :param soup: 解析后的soup对象
        :return: 返回有效数据
        '''
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', class_='lemma-summary')
        # 获取tag中包含的所有文本内容，包括子孙tag中的内容
        data['summary'] = summary.get_text()

        return data


