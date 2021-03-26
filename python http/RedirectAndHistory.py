import requests
# 将重定向字段设为True才可以通过r.history查看历史信息，即访问成功之前的所有请求跳转信息
r = requests.get('http://www.bilibili.com', allow_redirects=True)
print(r.url)
print(r.status_code)
print(r.history)


# 超时限制
requests.get('http://github.com', timeout=2)