'''
1.BeautifulSoup和lxml原理不同，BS基于DOM文档，会载入整个文档解析整个DOM树，在时间和内存的花费较大。
lxml使用XPath技术查询和处理HTML/XML文档的库，只会局部遍历，速度较快
2.BeautifulSoup使用较为简单，API非常人性化且支持CSS选择器。
lxml的XPath写起来麻烦
'''
from lxml import etree
html_str = '''
<html><head><title>The Dormouse's story</title></head>
<body>
<p class='title'><b>The Dormouse's story</b></p>
<p class='story'>Once upon a time there were three little sisters; and their names were
<a href='http://example.com/elsie' class='sister' id='link1'><!-- Elsie --></a>,
<a href='http://example.com/lacie' class='sister' id='link2'><!-- Lacie --></a>and
<a href='http://example.com/tillie' class='sister' id='link3'>Tillie</a>;
and they lived at the bottom of a well.</p>
<p class='story'>...</p>
'''
html = etree.HTML(html_str)
result = etree.tostring(html, pretty_print=True)    # 转化成字符串
print(result)           # 仍然补上了最后的</body>和</html>，HTML方法修正代码

# lxml还可以直接读取读取html文件
html = etree.parse(r'./index.html')
result = etree.tostring(html, pretty_print=True)
print(result)

# 用XPath语法抽取所有的URL
urls = html.xpath(".//*[@class='sister']/@href")      # 从根目录获取所有节点，然后找其中class='sister'的节点，然后提取它们的href
print(urls)

