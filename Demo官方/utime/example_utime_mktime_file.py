'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_mktime_file.py
'''
import utime
import log


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_mktime_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.INFO)
time_log = log.getLogger("MkTime")

if __name__ == '__main__':
    # 返回当前时间戳，参数为元组
    t = utime.mktime(utime.localtime())
    time_log.info(t)