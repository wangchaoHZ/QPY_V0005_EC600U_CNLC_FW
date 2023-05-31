# -*- coding: UTF-8 -*-


import utime
from usr import st7789v
from usr import image


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_ST7789V_LCD_Example"
PROJECT_VERSION = "1.0.0"

lcd_st7789v = st7789v.ST7789V(240, 240)


if __name__ == '__main__':
    '''######################【User code star】###################################################'''

    '''
    要显示的图片像素为 99*100，下面设置显示图片的起始坐标位置为（70，70）
    要注意：显示图片时，最后两个参数传入的是图片大小，即宽高，不是终点坐标
    '''
    lcd_st7789v.lcd_show_image(image.image_buf, 70, 70, 99, 100)

    '''######################【User code end 】###################################################'''
