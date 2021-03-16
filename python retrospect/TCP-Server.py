# coding:utf-8
import socket
import threading
import time


# TODO 处理用户连接
def dealClient(sock, addr):
    # 第四步：接收传来的数据，并发送给对方数据
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Hello, I am server!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        print('--->>%s!' % data.decode('utf-8'))
        sock.send(('Loop Msg: %s!' % data.decode('utf-8')).encode('utf-8'))
    # 第五步：关闭Socket
    sock.close()
    print('Connection from %s:%s closed' % addr)


if __name__ == '__main__':
    # 第一步：创建一个基于IPv4和TCP协议的socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    # 第二步：监听连接，看是否有客户端发起TCP连接请求
    s.listen(5)
    print('Waiting for connection...')
    while True:
        # 第三步：接收一个新连接
        sock, addr = s.accept()
        # 创建线程来处理TCP连接
        t = threading.Thread(target=dealClient, args=(sock, addr))
        t.start()

