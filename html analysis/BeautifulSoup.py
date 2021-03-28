# BeautifulSoup不仅支持python标准库中的html解析器，还支持lxml解析器，且lxml速度更快  pip install lxml不管用后使用pycharm自带安装
from bs4 import BeautifulSoup
import lxml
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
soup = BeautifulSoup(html_str, 'lxml', from_encoding='utf-8')   # 选择指定的解析器lxml来解析
print(soup.prettify())      # 格式化输出，html_str最后并没有</body>和</html>但lxml解析器仍然会补上


