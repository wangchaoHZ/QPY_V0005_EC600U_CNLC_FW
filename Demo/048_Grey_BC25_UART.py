import log
import utime
import checkNet
from machine import UART

state = 1
uart = None

# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_BC25_UART"
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
log.basicConfig(level=log.NOTSET)  # 设置日志输出级别
log = log.getLogger("Grey")  # 获取logger对象，如果不指定name则返回root对象，多次使用相同的name调用getLogger方法返回同一个logger对象


def uart_read():
    log.debug("uartread start!")
    global state
    global uart

    while 1:
        # while readnum:
        # readnum -= 1
        # 返回是否有可读取的数据长度
        msglen = uart.any()
        # 当有数据时进行读取
        if msglen:
            msglentemp = 0
            while msglentemp != msglen:
                msglentemp = msglen
                # log.debug("{}".format(msglentemp))
                utime.sleep_ms(100)
                msglen = uart.any()
            msg = uart.read(msglen)
            # 初始数据是字节类型（bytes）,将字节类型数据进行编码
            utf8_msg = msg.decode()
            if "Usart End" in utf8_msg:
                break
            else:
                log.info("uart_read msg: {}".format(utf8_msg))  # 发送数据
                uart.write("uart_read msg: {}".format(utf8_msg))  # 发送数据
            msglen = 0
    state = 0
    log.debug("uartread end!")


if __name__ == "__main__":
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    # utime.sleep(5)
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    # 【本例程可以屏蔽下面这一行！】
    checknet.wait_network_connected()
    log.debug("main start!")
    uart = UART(UART.UART1, 9600, 8, 0, 1, 0)  # EC600S/EC600N使用

    uart_read()

    while 1:
        if state:
            pass
        else:
            break
    log.debug("main end!")
