'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_sleep_file.py
'''
import utime
import log


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_sleep_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.INFO)
time_log = log.getLogger("Sleep")

if __name__ == '__main__':
    for i in [0, 1, 2, 3, 4, 5]:
        utime.sleep(1)   # 休眠(单位 m)
        time_log.info(i)

    for i in [0, 1, 2, 3, 4, 5]:
        utime.sleep_ms(1000)   # 休眠(单位 ms)
        time_log.info(i)
