# -*- coding: UTF-8 -*-
# 导入模块
import log
import utime
import ujson
import _thread
import checkNet
import ubinascii
from machine import UART

state = 1
band = 115200
uartport = UART.UART2
uart_x = None
usbcdc = None

# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Test"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# | 参数      | 参数类型 | 说明                | 类型      |
# | -------- | ------- | ------------------ | -------- |
# | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
# | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
# | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
# | INFO     | 常量     | 日志记录级别的数值 20 | info     |
# | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
# | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
# log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
# Grey_log = log.getLogger("Grey")


def uart_x_read():
    global state
    global band
    global uart_x
    global usbcdc
    global uartport

    while state:
        msglen = uart_x.any()  # 返回是否有可读取的数据长度
        if msglen:  # 当有数据时进行读取
            msg = uart_x.read(msglen)  # 读取数据
            utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            if "Grey" in utf8_msg:
                break
            elif 'SetBand:' in utf8_msg:
                band_temp = ubinascii.unhexlify(utf8_msg[8:])
                band = band_temp.decode()
                uart_x = UART(uartport, band, 8, 0, 1, 0)
            else:
                usbcdc.write("{}".format(utf8_msg))  # 发送数据
        utime.sleep_ms(1)
    state = 0


def usbcdc_read():
    global state
    global band
    global uart_x
    global usbcdc
    global uartport

    while state:
        msglen = usbcdc.any()  # 返回是否有可读取的数据长度
        if msglen:  # 当有数据时进行读取
            msg = usbcdc.read(msglen)  # 读取数据
            utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            if "Grey" in utf8_msg:
                break
            elif 'SetBand:' in utf8_msg:
                band_temp = ubinascii.unhexlify(utf8_msg[8:-2])
                band = band_temp.decode()
                uart_x.write("{}".format(band))  # 发送数据
                utime.sleep_ms(500)
                uart_x.close()
                uart_x = UART(uartport, int(band), 8, 0, 1, 0)
            else:
                uart_x.write("{}".format(utf8_msg))  # 发送数据
        utime.sleep_ms(1)
    state = 0


def uart_x_cb(para):
    global uart_x
    global usbcdc

    # usbcdc.write("{}".format(para))
    msg = uart_x.read(para[2])  # 读取数据
    utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
    usbcdc.write("{}".format(utf8_msg))  # 发送数据


def usbcdc_cb(para):
    global uart_x
    global usbcdc

    # uart_x.write("{}".format(para))
    msg = usbcdc.read(para[2])  # 读取数据
    utf8_msg = msg.decode()  # 初始数据是字节类型（bytes）,将字节类型数据进行编码
    uart_x.write("{}".format(utf8_msg))  # 发送数据


if __name__ == "__main__":
    # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时.
    # utime.sleep(5)
    # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息.
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功).
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected().
    # 注: 未插入SIM卡时函数不会阻塞.
    stagecode, subcode = checknet.wait_network_connected(120)
    # Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # # 网络已就绪: stagecode = 3, subcode = 1
    # # 没插sim卡: stagecode = 1, subcode = 0
    # # sim卡被锁: stagecode = 1, subcode = 2
    # # 超时未注网: stagecode = 2, subcode = 0
    # if stagecode != 3 or subcode != 1:
    #     Grey_log.warning('【Look Out】 Network Not Available\r\n')
    # else:
    #     Grey_log.error('【Look Out】 Network Ready\r\n')
    #
    # Grey_log.info('User Code Start\r\n\r\n')

    uart_x = UART(uartport, band, 8, 0, 1, 0)
    uart_x.set_callback(uart_x_cb)
    usbcdc = UART(UART.UART3, band, 8, 0, 1, 0)
    usbcdc.set_callback(usbcdc_cb)

    uart_x.write("Grey_UART_X测试")
    usbcdc.write("Grey_USBCDC测试")

    # _thread.start_new_thread(uart_x_read, ())  # 创建一个线程来监听接收uart消息
    # _thread.start_new_thread(usbcdc_read, ())  # 创建一个线程来监听接收CDC消息

    while state:
        utime.sleep_ms(1)

    Grey_log.info('User Code End\r\n\r\n')
