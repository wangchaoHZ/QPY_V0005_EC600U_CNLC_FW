# 导入模块
import usocket
import ujson
import log
import utime
import checkNet
import _thread
from machine import Pin
from machine import UART

socket = None
uart = None
state = 1


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Socket<=>UART"
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
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")


def debug():
    global state
    run_mun = 0

    while state:
        run_mun += 1
        Grey_log.info('Print run: {:04d}'.format(run_mun))
        utime.sleep_ms(1000)


def socket_read():
    global socket
    global uart
    global state

    while state:
        Grey_log.info('接收前')
        data = socket.recv(1024)
        Grey_log.info('接收后')
        if len(data) > 0 and 'TCPClient End' in data.decode():
            state = 0
            break
        if state == 0:
            break
        if len(data) > 0 and data.decode() != '[iotxx:ok]':
            Grey_log.info('----------------TCPclient Recv Data-----------------')
            Grey_log.info('TCPclient Recv Data: {}  Len: {:03d}\r\n'.format(data.decode(), len(data)))
            uart.write(data.decode())
        utime.sleep_ms(1)
    socket.close()  # 断开Socket连接
    Grey_log.info('========================TCPClient END========================\r\n')


def uart_read():
    global socket
    global uart
    global state

    while state:
        msglen = uart.any()  # 返回是否有可读取的数据长度
        if state == 0:
            break
        # 当有数据时进行读取
        if msglen:
            msg = uart.read(msglen)
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            if "Usart End" in utf8_msg:
                state = 0
            else:
                Grey_log.info('----------------Uart Recv Data-----------------')
                Grey_log.info('Uart Recv Data: {}  Len: {:03d}\r\n'.format(utf8_msg, len(utf8_msg)))
                socket.send("{}".format(utf8_msg))  # TCP发送数据
        else:
            utime.sleep_ms(1)
            continue
    uart.close()
    Grey_log.info('========================Uart END========================\r\n')


if __name__ == "__main__":
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    # checknet.wait_network_connected()
    Grey_log.info('========================Init========================\r\n')

    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)  # 创建一个Socket实例
    sockinfo = usocket.getaddrinfo('115.29.240.46', 9000)[0][-1]  # 解析域名
    socket.connect(sockinfo)  # 连接平台
    socket.send('ep=ABCDEF0123456789&pw=123456')  # 发送注册包信息连接设备
    connect_data = socket.recv(1024)  # 读取平台连接结果
    if connect_data.decode() == '[iotxx:ok]':  # 平台反馈连接成功
        Grey_log.info('TCPclient Connect OK\r\n')

    gpio11 = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PU, 0)  # 屏蔽GNSS模组干扰. EC600S/EC600N使用
    gpio11.write(1)  # 屏蔽GNSS模组干扰. EC600S/EC600N使用
    uart = UART(UART.UART1, 115200, 8, 0, 1, 0)  # 创建UART对象

    Grey_log.info('Init Config OK\r\n')

    # _thread.start_new_thread(debug, ())  # 创建一个线程
    _thread.start_new_thread(socket_read, ())  # 创建一个线程
    _thread.start_new_thread(uart_read, ())  # 创建一个线程
    while 1:
        if state:
            pass
        else:
            break
    Grey_log.info('========================Main END========================\r\n')
