# Pin使用示例

from machine import Pin
import utime


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Pin_example"
PROJECT_VERSION = "1.0.0"


'''
GPIO介绍：https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=pin
'''
gpio1 = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)

if __name__ == '__main__':
    gpio1.write(1) # 设置 gpio1 输出高电平
    val = gpio1.read() # 获取 gpio1 的当前高低状态
    print('val = {}'.format(val))
