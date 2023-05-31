"""
@Author: Kayden
@Date: 2021-10-12
@Description: example for LED
@FilePath: example_LED_file.py
"""
from machine import Pin
import utime

# EC600S/N模组
LED = Pin(Pin.GPIO24, Pin.OUT, Pin.PULL_DISABLE, 0)
# EC600U
# LED = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 0)
# BC25
# LED = Pin(Pin.GPIO5, Pin.OUT, Pin.PULL_DISABLE, 0)

if __name__ == '__main__':
    for i in range(10):
        LED.write(0)
        utime.sleep(1)
        LED.write(1)
        utime.sleep(1)
