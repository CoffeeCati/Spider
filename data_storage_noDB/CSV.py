from lxml import etree
import requests, csv, re
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0)'
headers = {'User-Agent': user_agent}
url = 'http://seputu.com/'
r = requests.get(url)
html = etree.HTML(r.text)

# 使用lxml处理
row = []        # 用于存放所有记录
# NOTE！！  xpath均返回list类型
div_mulus = html.xpath(".//*[@class='mulu']")   # 找到所有<div class='mulu'>标记
for div_mulu in div_mulus:
    div_h2 = div_mulu.xpath("./div[@class='mulu-title']/center/h2/text()")      # 找到<h2>标记的内容组成的list
    if len(div_h2) > 0:
        h2_title = div_h2[0]       # 提取标题的内容，一般list中就一个值，所以用[0]来取
        a_s = div_mulu.xpath("./div[@class='box']/ul/li/a")
        for a in a_s:
            href = a.xpath('./@href')[0]
            box_title = a.xpath('./@title')[0]      # 提取<a>标记的title属性值
            pattern = re.compile(r'\s*\[(?P<data>.*)\]\s+(?P<rtitle>.*)')  # 将title属性中的日期和标题分离出来
            match = pattern.search(box_title)
            if match != None:
                data = match.group('data')          # 日期
                real_title = match.group('rtitle')   # 标题
                content = (h2_title, real_title, href, data)    # 存放单条记录
                row.append(content)
header = ['Title', 'Real_Title', 'href', 'Data']
with open('./storage2.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    f_csv.writerows(row)


