import utime
import audio
from machine import Pin


def audio_cb(event):
    if event == 0:
        print('audio-play start.')
    elif event == 7:
        print('audio-play finish.')


def record_callback(args):
    global record
    print('file_name:{}'.format(args[0]))
    print('audio_len:{}'.format(args[1]))
    print('record_sta:{}'.format(args[2]))

    record_sta = args[2]
    if record_sta == 0:
        print('录音开始')
    elif record_sta == 3:
        print('录音完成')
        # ret = record.getFilePath("recordfile.wav")
        ret = record.getFilePath("recordfile.amr")
        print(ret)
        # 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
        aud = audio.Audio(0)
        aud.setVolume(11)
        aud.setCallback(audio_cb)
        ret = aud.play(1, 0, ret)
        if ret != 0:
            print("播放失败")
    elif record_sta == -1:
        print('录音错误！')


if __name__ == '__main__':
    print("录音实验")
    record = audio.Record()
    record.end_callback(record_callback)
    # ret = record.start('recordfile.wav', 30)  # 录制wav格式
    ret = record.start('recordfile.amr', 30)  # 录制amr格式
    if ret == 0:
        print("录音开始")
    else:
        print("录音失败")
    print("录音中......")
    utime.sleep_ms(10000) #录音10秒
    print("record.stop")
    record.stop() #录音10秒后，停止录音
    pass
#2022-01-10