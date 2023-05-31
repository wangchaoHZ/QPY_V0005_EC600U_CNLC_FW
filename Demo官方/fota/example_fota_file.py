'''
@Author: Pawn
@Date: 2020-07-28
@LastEditTime: 2020-11-30
@Description: example for module fota
@FilePath: example_fota_file.py
'''

import fota
import utime
import log
from misc import Power
import uos

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Fota_example"
PROJECT_VERSION = "1.0.0"

# 设置日志输出级别
log.basicConfig(level=log.INFO)
fota_log = log.getLogger("Fota")


# 此示例需要升级包文件（差分包等.bin文件）

def run():
    fota_obj = fota()  # 创建Fota对象
    file_size = uos.stat("FotaFile.bin")[6]  # 获取文件总字节数
    print(file_size)
    with open("FotaFile.bin", "rb") as f:  # rb模式打开.bin文件(需要制作升级包文件)
        while 1:
            c = f.read(1024)  # read
            if not c:
                break
            fota_obj.write(c, file_size)  # 写入.bin文件数据与文件总字节数

    fota_log.info("flush verify...")
    res = fota_obj.verify()  # 校验
    if res != 0:
        fota_log.error("verify error")
        return
    fota_log.info("flush power_reset...")
    utime.sleep(2)
    Power.powerRestart()  # 重启模块


if __name__ == '__main__':
    fota_log.info("run start...")
    run()
