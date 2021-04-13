'''
HTML正文主要存储为两种格式:JSON和CSV。
示例前提:静态网站，标题、章节、章节名称都不是由JavaScript动态加载
'''

# 存储为JSON
import requests
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0)'
headers = {'User-Agent': user_agent}
url = 'http://seputu.com/'
r = requests.get(url, headers=headers)
# print(r.text)

'''
    Pyhton对JSON文件的操作分为编码与解码，通过json模块来实现，编码过程是把python对象转换成JSON对象，常用的两个函数是dumps()、dump()
    dumps生成一个字符串，dump是通过fp文件流写入文件
    JSON文件的格式与字典类似  名称:值对
    dumps与dump函数原型：
    --->dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separator=None,
        encoding='utf-8', default=None, sort_keys=False, **kw)
    --->dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separator=None,
        encoding='utf-8', default=None, sort_keys=False, **kw)
        
    skipkeys: 默认值为False。如果dict的keys内的数据不是python的基本类型(str, unicode, int, long, float, bool ,None)，设置为
    False时就会报错TypeError，此时设置为True就会跳过这类key
    ensure_ascii: 默认值True。如果dict内有非ASCII字符，则会以"\\uXXXXX"的格式显示数据，设置为False后就能正常显示
    indent: 应该放置一个非负的整型，如果是0或者空，则一行显示数据，否则会换行且按照indent的值显示前边的后空，用于控制格式
    separators: 分隔符，实际上是(item_separator, dic_separator)元组，默认是(",", ":")表示keys之间使用","分隔，key和value之间用":"分隔
    sort_keys: 将数据根据keys进行排序
    
    
    解码过程常用函数有loads()、load()，其区别仍然是load()来处理文件，loads()直接处理字符串
    loads和load函数原型：
    --->loads(s, encoding=None, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
    --->load(fp, encoding=None, cls=None, object_hook=None, parse_float=None,
    parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)
    
    encoding: 指定编码格式
    parse_float: 如果指定，则将把每一个JSON字符串按照float解码调用。默认情况下这相当于float(num_str)
    parse_int: 如果指定，则把每一个JSON字符串按照int解码调用。默认情况下这相当于int(num_str)
'''
# 分析可知标题和章节都被包含在<dev class="mulu">下，标题位于<div class="mulu-title">下，章节位于<div class="box">下的<a>中
soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
content = []
for mulu in soup.find_all(class_='mulu'):
    h2 = mulu.find('h2')    # find()只返回第一个指定标记
    if h2 != None:
        h2_title = h2.string    # 获取标题
        ls = []
        for a in mulu.find(class_='box').find_all('a'):     # 找到<div class="box">下的所有<a>
            href = a.get('href')
            box_title = a.get('title')
            ls.append({"url": href, "box_title": box_title})
        content.append({"title": h2_title, "content": ls})

import json
with open('storage1.json', 'w') as fp:
    json.dump(content, fp=fp, indent=4, ensure_ascii=False)



