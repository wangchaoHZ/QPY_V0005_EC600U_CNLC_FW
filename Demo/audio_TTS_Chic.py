import audio


def tts_cb(event):
    if event == 2:
        print('TTS-play start.')
    elif event == 4:
        print('TTS-play finish.')


# 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
tts = audio.TTS(0) # 需要P40使能功放（EVB 2.0 J6-Pin10与Pin2短接）
# tts = audio.TTS(2) # 不需要功放，直接推动喇叭
tts.setCallback(tts_cb)
yue = "到账{}元".format(98.66)
tts.play(0, 0, 2, yue)

