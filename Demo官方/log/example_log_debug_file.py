import log
import utime


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Log_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.DEBUG)
# 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象
log = log.getLogger("debug")

if __name__ == '__main__':
    log.debug("Test debug message!!")
