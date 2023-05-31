import audio


def tts_cb(event):
    if event == 2:
        print('TTS-play start.')
    elif event == 4:
        print('TTS-play finish.')


# 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
tts = audio.TTS(0)
tts.setCallback(tts_cb)
yue = "到账{}元".format(98.66)
tts.play(0, 0, 2, yue)

