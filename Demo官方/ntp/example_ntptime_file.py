'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module ntptime
@FilePath: example_ntptime_file.py
'''
import ntptime
import log
import utime
import checkNet


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_NTP_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
ntp_log = log.getLogger("NtpTime")

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        ntp_log.info('Network connection successful!')

        # 查看默认ntp服务
        ntp_log.info(ntptime.host)
        # 设置ntp服务
        ntptime.sethost('pool.ntp.org')

        # 同步ntp服务时间
        ntptime.settime()
    else:
        ntp_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))