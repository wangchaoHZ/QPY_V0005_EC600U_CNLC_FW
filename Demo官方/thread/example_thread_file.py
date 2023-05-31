'''
@Author: Baron
@Date: 2020-06-22
@LastEditTime: 2020-06-22 17:16:20
@Description: example for module _thread
@FilePath: example_thread_file.py
'''
import _thread
import log
import utime

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Thread_example"
PROJECT_VERSION = "1.0.0"

# 设置日志输出级别
log.basicConfig(level=log.INFO)
thread_log = log.getLogger("Thread")

a = 0
state = 1
# 创建一个lock的实例
lock = _thread.allocate_lock()


def th_func(delay, id):
    global a
    global state
    while True:
        lock.acquire()  # 获取锁
        if a >= 10:
            thread_log.info('thread %d exit' % id)
            lock.release()  # 释放锁
            state = 0
            break
        a += 1
        thread_log.info('[thread %d] a is %d' % (id, a))
        lock.release()  # 释放锁
        utime.sleep(delay)


if __name__ == '__main__':
    for i in range(2):
        _thread.start_new_thread(th_func, (i + 1, i))  # 创建一个线程，当函数无参时传入空的元组

    while state:
        utime.sleep(1)  # 加个延时避免EC200U/EC600U运行重启
        pass
