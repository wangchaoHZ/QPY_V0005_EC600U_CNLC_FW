import utime as time
import _thread
import modem
import sim
import net
import checkNet
from umqtt import MQTTClient
import ujson
from machine import Timer

mqtt = None
lock = None
timer = None
timer_num = 0

PROJECT_NAME = "Grey_ONENET_MQTT"
PROJECT_VERSION = '1.0.1'
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

SubTopic = "app_topic"  # 订阅的主题
PubTopic = "kfb_topic"  # 发布的主题


def sub_cb(topic, msg):
    cmd = ujson.loads(msg)
    print('接收主题{}的信息: {}'.format(topic, cmd))


def mqtt_config():
    global mqtt
    global SubTopic

    mqtt = MQTTClient(client_id="629548131", server="183.230.40.39", port=6002,
                      user="362586", password="ceshi_1", keepalive=60)
    mqtt.set_callback(sub_cb)
    mqtt.connect()
    mqtt.subscribe(SubTopic)


def wait_msg_task():  # 获取msg消息
    global mqtt
    if mqtt is not None:
        while True:
            mqtt.wait_msg()
            time.sleep_ms(100)


# def get_mqttstatue():  # 判断MQTT连接状态, 进行重连
#     global mqtt
#     global lock
#     global SubTopic
#     global timer
#
#     while True:
#         rst = mqtt.get_mqttsta()
#         if rst != 0:
#             timer.stop()
#             lock.acquire()                      # 获取锁
#             print('MQTT状态异常，状态码:{}, 等待重启'.format(rst))
#             if rst == -1:
#                 mqtt = MQTTClient(client_id="629548131", server="183.230.40.39", port=6002,
#                                   user="362586", password="ceshi_1", keepalive=60)
#                 print('1-1')
#                 mqtt.set_callback(sub_cb)  # 设置回调
#                 print('1-2')
#                 mqtt.connect()
#                 print('1-3')
#                 mqtt.subscribe(SubTopic)
#                 print('1-4')
#             else:
#                 mqtt.disconnect()  # 断开MQTT连接
#                 print('2-1')
#                 mqtt = MQTTClient(client_id="629548131", server="183.230.40.39", port=6002,
#                                   user="362586", password="ceshi_1", keepalive=60)
#                 print('2-2')
#                 mqtt.set_callback(sub_cb)  # 设置回调
#                 print('2-3')
#                 mqtt.connect()
#                 print('2-4')
#                 mqtt.subscribe(SubTopic)
#                 print('2-5')
#             timer.start(period=10000, mode=timer.PERIODIC, callback=timer_task)
#             lock.release()  # 释放锁
#         else:
#             time.sleep_ms(1000)
#             pass


def timer_task(args):               # 获取设备的IMEI,固件版本号,sim卡的iccid号
    global mqtt
    global PROJECT_VERSION
    global timer_num
    global PubTopic

    timer_num += 1
    net_value = net.csqQueryPoll()
    # dev_imei = modem.getDevImei()
    # dev_fw_version = modem.getDevFwVersion()
    # sim_iccid = sim.getIccid()
    # print('固件版本: {}\r\n软件版本: {}\r\n设备IMEI: {}\r\nsim卡iccid: {}\r\n信号强度: {}\r\n{}'.
    #       format(dev_fw_version, PROJECT_VERSION, dev_imei, sim_iccid, net_value, args))
    # if timer_num == 6:
    #     timer_num = 0
    #     data = {'dev_imei': dev_imei,
    #             'dev_fw_version': dev_fw_version,
    #             'sim_iccid': sim_iccid,
    #             'PROJECT_VERSION': PROJECT_VERSION,
    #             'net_value': net_value
    #             }
    #     print(ujson.dumps(data))
    #     mqtt.publish(PubTopic, ujson.dumps(data))
    print('信号强度: {}\r\n{}'.format(net_value, args))
    if timer_num == 6:
        timer_num = 0
        data = {'net_value': net_value}
        mqtt.publish(PubTopic, ujson.dumps(data))


if __name__ == "__main__":
    # 手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    # 否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    time.sleep(5)
    checknet.poweron_print_once()
    # 如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    # 如果是网络无关代码，可以屏蔽 wait_network_connected()
    checknet.wait_network_connected()

    lock = _thread.allocate_lock()  # 创建互斥锁
    mqtt_config()
    _thread.start_new_thread(wait_msg_task, ())
    # _thread.start_new_thread(get_mqttstatue, ())
    timer = Timer(Timer.Timer1)
    timer.start(period=10000, mode=timer.PERIODIC, callback=timer_task)
