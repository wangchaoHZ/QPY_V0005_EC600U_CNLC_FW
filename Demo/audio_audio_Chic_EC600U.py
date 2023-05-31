import audio

def audio_cb(event):
    if event == 0:
        print('audio-play start.')
    elif event == 7:
        print('audio-play finish.')

# 设备类型，0 - 听筒，1 - 耳机，2 - 喇叭
aud = audio.Audio(0) # 需要P40使能功放（EVB 2.0 J6-Pin10与Pin2短接）
# aud = audio.Audio(2) # 不需要功放，直接推动喇叭
aud.setCallback(audio_cb)
ret = aud.play(1, 0, 'U:/audio_audio_haixiu.mp3')
print(ret)
ret = aud.play(1, 0, 'U:/audio_audio_haixiu.wav')
print(ret)

# aud.setVolume(11) #音量等级，范围（1 ~ 11），数值越大，音量越大

#2022-01-10


