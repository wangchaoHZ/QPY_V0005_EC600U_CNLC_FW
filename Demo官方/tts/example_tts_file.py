'''
@Author: Kayden
@Date: 2021-10-13
@Description: example for module TTS
@FilePath: example_tts_file.py
'''
import log
from audio import TTS
import utime
from machine import Pin

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_TTS_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.INFO)
tts_Log = log.getLogger("TTS")


if __name__ == '__main__':
    # 参数1：device （0：听筒，1：耳机）
    tts = TTS(0)
    '''
    开发板外接喇叭播放时，需要使能对应的引脚才能发声，具体看开发板原理图
    EC600X_QuecPython_EVB_V1.3和EC600X_QuecPython_EVB_V2.0均为PIN40引脚
    '''
    # EC600S/EC600N的PIN40对应GPIO9
    TTS_EN = Pin(Pin.GPIO9, Pin.OUT, Pin.PULL_PU, 1)
    
    # 获取当前播放音量大小
    volume_num = tts.getVolume()
    tts_Log.info("Current TTS volume is %d" %volume_num)

    # 设置音量为6
    volume_num = 8
    tts.setVolume(volume_num)
    #  参数1：优先级 (0-4)
    #  参数2：打断模式，0表示不允许被打断，1表示允许被打断
    #  参数3：模式 （1：UNICODE16(Size end conversion)  2：UTF-8  3：UNICODE16(Don't convert)）
    #  参数4：数据字符串 （待播放字符串）
    tts.play(1, 1, 2, '移远通信') # 执行播放
    tts.close()   # 关闭TTS功能
