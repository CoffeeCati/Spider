import requests
r = requests.get('http://www.baidu.com')
print('content-->' + str(r.content))
print('text-->' + r.text)                   # 中文会变成乱码
print('encoding-->' + r.encoding)
r.encoding = 'utf-8'
print('new text-->' + r.text)               # 指定编码方式为utf-8后变为正常


# 解决方法，使用chardet模块，pip install --upgrade pip 更新pip  >  pip install chardet
import chardet
print(chardet.detect(r.content))   # 返回字典{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
r.encoding = chardet.detect(r.content)['encoding']
print(r.text)


# 解决方法，流方式
sr = requests.get('http://www.baidu.com', stream=True)
print(sr.raw.read(10))

