# 导入模块
import pm
import log
import utime
import ujson
import _thread
import checkNet
from machine import Pin
from machine import RTC
from machine import UART
from machine import Timer


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_BC25_PM"
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


def rtc_cb(args):
    from machine import RTC
    print("[RTC_Callback]: {}".format(rtc.datetime()))


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

    rtc = RTC()  # 创建对象
    rtc.register_callback(rtc_cb)  # 设置回调函数

    data_e = rtc.datetime()  # 设置/获取RTC
    data_l = list(data_e)  # 将元组转换成列表, 元组的元素不能修改, 固转换成列表.
    data_l[5] += 5  # 分
    if data_l[6] > 60:  # 秒
        data_l[6] -= 60  # 秒
        data_l[5] += 1  # 分
    if data_l[5] > 60:  # 分
        data_l[5] -= 60  # 分
        data_l[4] += 1  # 时
    if data_l[4] > 24:  # 时
        data_l[4] -= 24  # 时
        data_l[3] += 1  # 星期
        data_l[2] += 1  # 天
    if data_l[3] > 7:  # 星期
        data_l[3] -= 7  # 星期

    data_e = tuple(data_l)  # 将列表转换成元组
    rtc.set_alarm(data_e)  # 设置RTC警报时间
    rtc.enable_alarm(1)  # 启动/停止RTC
    Grey_log.critical("[Present_Time]: {}".format(data_e))

    Grey_log.info('User Code End\r\n\r\n')
    utime.sleep_ms(1000)
    pm.autosleep(1)  # 设置自动休眠模式
