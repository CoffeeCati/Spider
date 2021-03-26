import requests
r = requests.get('http://www.baidu.com')
if r.status_code == requests.codes.ok:
    print(r.status_code)    # 响应码
    print(r.headers)    # 响应头
    print(r.headers.get('content-type'))    # 获取指定内容，推荐
    print(r.headers['content-type'])         # 获取指定内容，不推荐
else:
    r.raise_for_status()        # 当响应码为4XX或5XX时raise_for_status()会抛出异常否则返回None
