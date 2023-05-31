"""
运行本例程，需要通过串口线连接开发板的串口2排针（TX2和RX2）和PC，在PC上通过串口工具
打开串口，并向该端口发送数据，即可看到 PC 发送过来的消息。
"""
import _thread
import utime
import log
from machine import UART

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_UART_example"
PROJECT_VERSION = "1.0.0"

'''
串口数量及对应引脚号查看API介绍：
https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=uart
'''

# 设置日志输出级别
log.basicConfig(level=log.INFO)
uart_log = log.getLogger("UART")

state = 5


def uartWrite():
    count = 10
    # 配置uart
    uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
    while count:
        write_msg = "Hello count={}".format(count)
        # 发送数据
        uart.write(write_msg)
        uart_log.info("Write msg :{}".format(write_msg))
        utime.sleep(1)
        count -= 1
    uart_log.info("uart2Write end!")
    # 及时关闭避免重复打开报错
    uart.close()


def UartRead():
    global state
    uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
    while 1:
        utime.sleep_us(1)  # 加个延时避免EC200U/EC600U运行重启
        # 返回是否有可读取的数据长度
        msgLen = uart.any()
        # 当有数据时进行读取
        if msgLen:
            msg = uart.read(msgLen)
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            # str
            uart_log.info("UartRead msg: {}".format(utf8_msg))
            state -= 1
            if state == 0:
                break
        else:
            continue
    # 及时关闭避免重复打开报错
    uart.close()


def run():
    # 创建一个线程来监听接收uart消息
    _thread.start_new_thread(UartRead, ())


if __name__ == "__main__":
    uartWrite()
    run()
    while 1:
        if state:
            utime.sleep_us(1)  # 加个延时避免EC200U/EC600U运行重启
            pass
        else:
            break

# 运行结果示例
'''
INFO:UART:Write msg :Hello count=8
INFO:UART:Write msg :Hello count=7
INFO:UART:Write msg :Hello count=6
INFO:UART:Write msg :Hello count=5
INFO:UART:Write msg :Hello count=4
INFO:UART:Write msg :Hello count=3
INFO:UART:Write msg :Hello count=2
INFO:UART:Write msg :Hello count=1
INFO:UART:uartWrite end!
INFO:UART:UartRead msg: read msg 1

INFO:UART:UartRead msg: read msg 2

INFO:UART:UartRead msg: read msg 3
'''
