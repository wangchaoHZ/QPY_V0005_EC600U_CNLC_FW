
import audio
from machine import Pin

# you_238_SPK = Pin(Pin.GPIO11, Pin.OUT, Pin.PULL_PU, 1)  # SPK使能
# you_238_SPK.write(1)
# tts = audio.TTS(2)          # 创建TTS对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
# play = audio.Audio(2)       # 创建播放对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭

tts = audio.TTS(0)          # 创建TTS对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
play = audio.Audio(0)       # 创建播放对象, 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭

tts.setVolume(9)    # 设置音量值，音量值为0~9，0表示静音
print('\r\n')
print('当前音量值: {}'.format(tts.getVolume()))  # 获取音量值
play.setVolume(1)  # 设置音量值，音量值为1~11，0表示静音
print('\r\n')
print('当前音量值: {}'.format(play.getVolume()))  # 获取音量值

str1 = '[m51]可以获取地[=di4]图上任意地[=di4]点的坐标,同样也可以根据已有的经纬度坐标定位到实际位置.'
tts.play(4, 0, 2, str1)

# tts的多音字和数字号码数值
tts.play(0, 0, 2, '[m52]几单[=dan1] 姓单[=shan4] 单[=chan2]于[=yu2]')
tts.play(0, 0, 2, '[m53][n1]1234567')  # 数字作号码处理
tts.play(0, 0, 2, '[m54][n2]1234567')  # 数字作数值处理
tts.play(4, 0, 2, '[m55]可以获取地[=di4]图上任意地[=di4]点的坐标,同样也可以根据已有的经纬度坐标定位到实际位置.')

# n1 - 数字作号码处理
# n2 - 数字作数值处理
# m51 – 许久
# m52 – 许多
# m53 – 晓萍
# m54 – 唐老鸭
# m55 – 许宝宝