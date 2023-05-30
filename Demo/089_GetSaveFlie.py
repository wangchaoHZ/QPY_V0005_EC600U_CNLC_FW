# -*- coding: UTF-8 -*-
# 导入模块 & 全局变量
if True:  # 方便代码折叠, 可不要. 
    import log, utime, ujson, _thread, checkNet, request, ujson


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


   
    flie_data = bytearray(10000)  # 为文件缓存预留空间 
    url = "http://112.31.84.164:8300/upload/Grey/000_Grey_Test.py"


# 线程保护测试例程
def Grey():
    a = 0
    while True:
        print('Grey running: {}'.format(a))
        a += 1
        if a >= 5:
            _thread.delete_lock(0)  # 就是为了抛异常
            break
        utime.sleep_ms(1000)


# 线程监控函数, 实际线程以参数传入
def thread(func):
    global Grey_log
    while True:
        try:
            func()
        except Exception as e:
            Grey_log.error(
                "{}Because of the[{}] caught exception,restart now!!!!".format(func, e))
        finally:
            Grey_log.critical('End of the thread\r\n\r\n')
            pass  # 客户自己实现


def getsaveflie(url, flie="/usr/test.txt"):
    global flie_data
    flie_data = ''
    response = request.get(url=url)
    for i in response.text:
        flie_data = flie_data+i
    Grey_log.debug(flie_data)
    f = open(flie, 'w')
    f.write(flie_data)
    f.close()


if __name__ == "__main__":
    utime.sleep(5)  # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时.
    checknet.poweron_print_once()  # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息.

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功).
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected().
    # 注: 未插入SIM卡时该函数可能不会阻塞. 
    stagecode, subcode = checknet.wait_network_connected(30)
    Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # 网络已就绪: stagecode = 3, subcode = 1
    # 没插sim卡: stagecode = 1, subcode = 0
    # sim卡被锁: stagecode = 1, subcode = 2
    # 超时未注网: stagecode = 2, subcode = 0
    if stagecode != 3 or subcode != 1:
        Grey_log.warning('【Look Out】 Network Not Available\r\n')
    else:
        Grey_log.error('【Look Out】 Network Ready\r\n')

    # _thread.start_new_thread(thread, (Grey,))  # 线程保护测试示例, 实际使用请注释.

    Grey_log.info('User Code Start\r\n\r\n')

    getsaveflie(url, "/usr/Grey_Test.py")

    Grey_log.info('User Code End\r\n\r\n')

