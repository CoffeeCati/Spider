# coding:utf-8
import socket

# 创建socket，绑定指定的IP和端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))     # TCP和UDP绑定同一端口9999不会冲突
print('bind UDP on 9999...')
while True:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s' % addr)
    s.sendto(b'Hello, %s!' % data, addr)


