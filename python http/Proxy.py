# 设置proxies参数来配置单个请求
import requests, chardet
proxies = {
    'http': 'http://0.10.1.10:3132',
    'https': 'https://10.10.1.10:1080'
}
r = requests.get('http://example.org', proxies=proxies)
r.encoding = chardet.detect(r.content)['encoding']
print(r.text)

# 可以通过环境变量HTTP_PROXY和HTTPS_PROXY来配置代理，可以使用http://user:password@host/语法
proxies = {
    'http': 'http://user:password@10.10.1.10:3128'
}

