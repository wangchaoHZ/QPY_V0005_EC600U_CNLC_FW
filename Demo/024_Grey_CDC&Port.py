# import log
import utime
import _thread
import ubinascii
from machine import UART

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
    uart_x = UART(UART.UART2, 115200, 8, 0, 1, 0)
    usbcdc = UART(UART.UART3, 115200, 8, 0, 1, 0)
    uart_x.control_485(UART.GPIO38, 1)

    uart_x.write("Grey_测试")
    usbcdc.write("Grey_测试") 

    _thread.start_new_thread(uart_x_read, ())  # 创建一个线程来监听接收uart消息
    _thread.start_new_thread(usbcdc_read, ())  # 创建一个线程来监听接收CDC消息

    while state:
        utime.sleep_ms(1)
