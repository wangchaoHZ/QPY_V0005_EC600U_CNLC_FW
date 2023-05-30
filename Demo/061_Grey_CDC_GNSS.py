# import log
import utime
import _thread
import ubinascii
from machine import UART
from machine import Pin

state = 1
uart_x = None
usbcdc = None

# # | 参数      | 参数类型 | 说明                |
# # | -------- | ------- | ------------------ |
# # | CRITICAL | 常量     | 日志记录级别的数值 50 |
# # | ERROR    | 常量     | 日志记录级别的数值 40 |
# # | WARNING  | 常量     | 日志记录级别的数值 30 |
# # | INFO     | 常量     | 日志记录级别的数值 20 |
# # | DEBUG    | 常量     | 日志记录级别的数值 10 |
# # | NOTSET   | 常量     | 日志记录级别的数值 0  |
# log.basicConfig(level=log.CRITICAL)  # 设置日志输出级别
# log = log.getLogger("Grey")  # 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象


def uart_x_read():
    global state
    global uart_x
    global usbcdc

    while state:
        msglen = uart_x.any()  # 返回是否有可读取的数据长度
        if msglen:  # 当有数据时进行读取
            msg = uart_x.read(msglen)  # 读取数据
            utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            if "Grey" in utf8_msg:
                break
            else:
                usbcdc.write("{}".format(utf8_msg))  # 发送数据
        utime.sleep_ms(1)
    state = 0


def usbcdc_read():
    global state
    global uart_x
    global usbcdc

    while state:
        msglen = usbcdc.any()  # 返回是否有可读取的数据长度
        if msglen:  # 当有数据时进行读取
            msg = usbcdc.read(msglen)  # 读取数据
            utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            if "Grey" in utf8_msg:
                break
            else:
                uart_x.write("{}".format(utf8_msg))  # 发送数据
        utime.sleep_ms(1)
    state = 0


if __name__ == "__main__":
    gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PU, 1)  # V1.2使能
    gpio14 = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_PU, 1)  # 复位引脚
    gpio15 = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_PU, 1)
    gpio18 = Pin(Pin.GPIO18, Pin.OUT, Pin.PULL_PD, 0)
    uart_x = UART(UART.UART2, 9600, 8, 0, 1, 0)
    uart_x.write("$CFGNAV,10000,10000,3\r\n")  # L76C吐频率
    utime.sleep_ms(200)
    uart_x.write("$CFGPRT,1,0,115200,1,3\r\n")  # L76C修改波特率115200
    utime.sleep_ms(200)
    uart_x.write("$PCAS01,5*19\r\n")  # L76K修改波特率115200
    utime.sleep_ms(500)
    uart_x.close()
    uart_x = UART(UART.UART2, 115200, 8, 0, 1, 0)
    usbcdc = UART(UART.UART3, 115200, 8, 0, 1, 0)

    uart_x.write("Grey_UART_X测试")
    usbcdc.write("Grey_USBCDC测试")

    _thread.start_new_thread(uart_x_read, ())  # 创建一个线程来监听接收uart消息
    _thread.start_new_thread(usbcdc_read, ())  # 创建一个线程来监听接收CDC消息

    while state:
        utime.sleep_ms(1)
