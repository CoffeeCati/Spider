import requests
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0)'
headers = {'User-Agent': user_agent}
r = requests.get('http://www.baidu.com', headers=headers)
print(r.content.decode('utf-8'))
