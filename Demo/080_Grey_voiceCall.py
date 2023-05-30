# -*- coding: UTF-8 -*-
# 导入模块
import log
import utime
import ujson
import audio
import _thread
import checkNet
import voiceCall


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Test"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# | Parameter | parameter | description               | type     |
# | --------- | --------- | ------------------------- | -------- |
# | CRITICAL  | constant  | value of logging level 50 | critical |
# | ERROR     | constant  | value of logging level 40 | error    |
# | WARNING   | constant  | value of logging level 30 | warning  |
# | INFO      | constant  | value of logging level 20 | info     |
# | DEBUG     | constant  | value of logging level 10 | debug    |
# | NOTSET    | constant  | value of logging level 0  | notset   |

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

tts = None
str1 = "客户: "
str2 = "来电, 请接听. "


def dtmf_cb(args):
    print(args)


def voice_callback(args):
    global tts, str1, str2

    if args[0] == 10:
        print('voicecall incoming call, PhoneNO.: ', args[6])
        str3 = "[n1]"+ args[6][2:-1]
        tts.stopAll()
        tts.play(4, 0, 2, str1+str3+str2)
    elif args[0] == 11:
        print('voicecall connected, PhoneNO.: ', args[6])
        # voiceCall.startDtmf("1234567890*#", 1000)   # 设置DTMF音
        #                                             # 参数一: DTMF字符串。最大字符数：32个。有效字符数有：0、1、…、9、A、B、C、D、*、#
        #                                             # 参数二: 持续时间。范围：100-1000；单位：毫秒。
    elif args[0] == 12:
        print('voicecall disconnect')
    elif args[0] == 13:
        print('voicecall is waiting, PhoneNO.: ', args[6])
    elif args[0] == 14:
        print('voicecall dialing, PhoneNO.: ', args[6])
    elif args[0] == 15:
        print('voicecall alerting, PhoneNO.: ', args[6])
    elif args[0] == 16:
        print('voicecall holding, PhoneNO.: ', args[6])


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

    record = audio.Record()
    record.gain(4, 12)

    tts = audio.TTS(0)
    voiceCall.setCallback(voice_callback)  # 注册监听回调函数
    voiceCall.dtmfSetCb(dtmf_cb)  # 设置DTMF识别回调
    voiceCall.dtmfDetEnable(1)  # 使能DTMF音
    # voiceCall.setFw(3, 1, "xxx-xxxx-xxxx")  # 设置控制呼叫转移
    # voiceCall.setChannel(0)  # 切换音频通道
    voiceCall.setVolume(11)  # 设置音量大小, 最大11 
    # voiceCall.getVolume()  # 获取音量大小
    # voiceCall.setAutoRecord(1, 1, 2, "U:/test.amr")  # 自动录音
    # voiceCall.startRecord(0, 2, "U:/test.amr")  # 开启录音
    # oiceCall.stopRecord()  # 结束录音
    voiceCall.setAutoAnswer(30)  # 设置自动应答时间, 单位: S 

    voiceCall.callStart("18356093181")  # Grey
    # voiceCall.callStart("15173402357")  # 客户号码
    # voiceCall.callStart("13681693100")  # 客户号码
    # voiceCall.callStart("13468671396")  # Jouni
    # voiceCall.callStart("18340890698")  # Kelly

    # voiceCall.callAnswer()  # 接听电话
    # voiceCall.callEnd()  # 挂断电话
    
    Grey_log.info('User Code End\r\n\r\n')
