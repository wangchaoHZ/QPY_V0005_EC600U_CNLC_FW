# -*- coding: UTF-8 -*-


import utime
from usr import st7789v

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_ST7789V_LCD_Example"
PROJECT_VERSION = "1.0.0"

lcd_st7789v = st7789v.ST7789V(240, 240)


if __name__ == '__main__':
    # 用户代码
    '''######################【User code star】###################################################'''
    fc = 0x0000  # 字体颜色 黑色 可根据需要修改
    bc = 0xffff  # 背景颜色 白色 可根据需要修改

    # 8x16 ASCII字符显示
    lcd_st7789v.lcd_show_ascii(0, 0, 8, 16, 'A', fc, bc)
    lcd_st7789v.lcd_show_ascii(8, 0, 8, 16, 'b', fc, bc)
    lcd_st7789v.lcd_show_ascii(16, 0, 8, 16, '$', fc, bc)
    lcd_st7789v.lcd_show_ascii(24, 0, 8, 16, '8', fc, bc)

    # 16x24 ASCII字符显示
    lcd_st7789v.lcd_show_ascii(0, 20, 16, 24, 'A', fc, bc)
    lcd_st7789v.lcd_show_ascii(16, 20, 16, 24, 'b', fc, bc)
    lcd_st7789v.lcd_show_ascii(32, 20, 16, 24, '$', fc, bc)
    lcd_st7789v.lcd_show_ascii(48, 20, 16, 24, '8', fc, bc)

    # 16x16 汉字显示
    lcd_st7789v.lcd_show_chinese(0, 50, 16, 16, '移', fc, bc)
    lcd_st7789v.lcd_show_chinese(16, 50, 16, 16, '远', fc, bc)
    lcd_st7789v.lcd_show_chinese(32, 50, 16, 16, '通', fc, bc)
    lcd_st7789v.lcd_show_chinese(48, 50, 16, 16, '信', fc, bc)

    # # 16x24 汉字显示
    lcd_st7789v.lcd_show_chinese(0, 70, 16, 24, '移', fc, bc)
    lcd_st7789v.lcd_show_chinese(16, 70, 16, 24, '远', fc, bc)
    lcd_st7789v.lcd_show_chinese(32, 70, 16, 24, '通', fc, bc)
    lcd_st7789v.lcd_show_chinese(48, 70, 16, 24, '信', fc, bc)

    '''######################【User code end 】###################################################'''
