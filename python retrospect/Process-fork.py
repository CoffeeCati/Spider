'''
pyhton3 实现多进程方式：
1. Unix/Linux/MacOS 独有的方式：os模块中的fork
2. 跨平台方式：使用multiprocessing模块
'''
# os 模块中的 fork 方法来源于Unix/Linux系统中的fork系统调用，调用一次返回两次。原因是当前进程复制出一份几乎相同的子进程，
# 子进程永远返回0，而当前进程(父进程)返回子进程的ID，注意不要与os.getpid()弄混淆
import os
if __name__ == '__main__':
    print('current Process (%s)  start ...' % (os.getpid()))   # os.getpid()获取当前进程ID
pid = os.fork()     # fork调用一次返回两次 <!-- 相当于获取当前进程的子进程ID -->
if pid < 0:
    print('Error in fork')
elif pid == 0:
    print("I'm child process(%s) and my parent process is (%s)" % (os.getpid(), os.getppid()))
else:
    print('I(%s) created a child process (%s)' % (os.getpid(), pid))


