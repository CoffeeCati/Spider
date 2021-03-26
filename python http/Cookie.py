import requests
# 获取响应中包含的cookie的值
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0)'
headers = {'User-Agent': user_agent}
r = requests.get('https://www.baidu.com', headers=headers)
for cookie in r.cookies.keys():
    print(cookie + ': ' + r.cookies.get(cookie))


# 自定义cookie值发出去
cookies = dict(name='qiye', age='10')
rr = requests.get('http://www.baidu.com', headers=headers, cookies=cookies)
print(rr.text)


# 使用requests提供的session实现连续访问网页，在处理登录跳转非常方便，程序自动把cookie带上，无需关心cookie的值时可以使用该方法
loginUrl = 'https://www.xxxxx.com/login'
s = requests.session()
# 首先访问登陆界面，服务器会先分配一个cookie
sr = s.get(loginUrl, allow_redirects=True)  # allow_redirects重定向字段
datas = {'name': 'userName', 'passwd': 'password'}
sr = s.post(loginUrl, data=datas, allow_redirects=True)
print(sr.text)

