'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2021-10-13
@Description: example for module timer
@FilePath: example_timer_file.py
'''
import log
import utime
from machine import Timer

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Timer_example"
PROJECT_VERSION = "1.0.0"

# 设置日志输出级别
log.basicConfig(level=log.INFO)
Timer_Log = log.getLogger("Timer")

num = 0
state = 1
# 注：支持定时器Timer0~Timer3
t = Timer(Timer.Timer1)


# 创建一个执行函数，并将timer实例传入
def timer_test(t):
    global num
    global state
    Timer_Log.info('num is %d' % num)
    num += 1
    if num > 10:
        Timer_Log.info('num > 10, timer exit')
        state = 0
        t.stop()  # 结束该定时器实例


if __name__ == '__main__':
    t.start(period=1000, mode=t.PERIODIC, callback=timer_test)  # 启动定时器

    while state:
		utime.sleep(1)  # 加个延时避免EC200U/EC600U运行重启
        pass
