# 导入模块
import log
import utime
import ujson
import _thread
import checkNet
from machine import Pin
from machine import LCD
from machine import UART
from machine import Timer


num = 0
state = 1
uart = None
Hex_Data = '\xab\xcd\xef\x12\x34\x56\x78\x90\xAB\xCD\xEF'


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
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")


# 创建一个执行函数，并将timer实例传入
def grey_timer(args):
    global num
    global Hex_Data

    num += 1
    uart.write("{}".format(Hex_Data))
    Grey_log.info('Grey timer exit num: {:04d}'.format(num))
    Grey_log.info(args)


def uart_read():
    Grey_log.debug("uartread start!")
    global state
    global uart

    while 1:
        # while readnum:
        # readnum -= 1
        # 返回是否有可读取的数据长度
        msglen = uart.any()
        # 当有数据时进行读取
        if msglen:
            msg = uart.read(msglen)
            # print(type(msg))
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            if "Usart End" in utf8_msg:
                break
            else:
                # 发送数据
                Grey_log.info("uartread msg: {}".format(utf8_msg))
                uart.write("uartread msg: {}".format(utf8_msg))
        else:
            utime.sleep_ms(1)
            continue
    state = 0
    Grey_log.debug("uartread end!")


if __name__ == "__main__":
    # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时.
    # utime.sleep(5)
    # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息.
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功).
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected().
    # 注: 未插入SIM卡时函数不会阻塞.
    stagecode, subcode = checknet.wait_network_connected(120)
    Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # 网络已就绪: stagecode = 3, subcode = 1
    # 没插sim卡: stagecode = 1, subcode = 0
    # sim卡被锁: stagecode = 1, subcode = 2
    # 超时未注网: stagecode = 2, subcode = 0
    if stagecode != 3 or subcode != 1:
        Grey_log.warning('【Look Out】 Network Not Available\r\n')
    else:
        Grey_log.error('【Look Out】 Network Ready\r\n')

    Grey_log.info('User Code Start\r\n\r\n')

    time = Timer(Timer.Timer1)
    time.start(period=5000, mode=time.PERIODIC, callback=grey_timer)  # 启动定时器
    # time.stop()  # 结束该定时器实例

    uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
    uart.control_485(UART.GPIO38, 1)
    _thread.start_new_thread(uart_read, ())  # 创建一个线程来监听接收uart消息
    uart.write("{}".format(Hex_Data))
