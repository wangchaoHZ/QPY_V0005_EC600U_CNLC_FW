"""
本例程选择播放haixiu.mp3，运行前将音频文件下载进模组
开发板外接喇叭播放时，需要使能对应的引脚才能发声，具体看开发板原理图
EC600X_QuecPython_EVB_V1.3和EC600X_QuecPython_EVB_V2.0均为PIN40引脚
"""
import audio
from machine import Pin
# EC600S/EC600N的PIN40对应GPIO9
# EC600U只能通过杜邦线连接PIN40的排针和3.3V排针
audio_EN = Pin(Pin.GPIO9, Pin.OUT, Pin.PULL_PU, 1)
# 参数1：device 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
aud = audio.Audio(0)
#  参数1：播放优先级，支持优先级0~4，数值越大优先级越高
#  参数2：打断模式，0表示不允许被打断，1表示允许被打断
#  参数3：待播放的文件名称，包含文件存放路径
aud.play(2, 1, 'U:/haixiu.mp3')
