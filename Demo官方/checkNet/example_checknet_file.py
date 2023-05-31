"""
@Author: jayceon
@Date: 2021-03-25
@LastEditTime: 2021-03-25
@Description: example for module checkNet
@FilePath: example_checknet_file.py
"""

import usocket
import log
import utime
import checkNet


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_checkNet_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
checknet_log = log.getLogger("CheckNet")

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        checknet_log.info('Network connection successful!')
        checknet.poweron_print_once()

        # 创建一个socket实例
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        # 解析域名
        sockaddr=usocket.getaddrinfo('www.tongxinmao.com', 80)[0][-1]
        # 建立连接
        sock.connect(sockaddr)
        # 向服务端发送消息
        ret=sock.send('GET /News HTTP/1.1\r\nHost: www.tongxinmao.com\r\nAccept-Encoding: deflate\r\nConnection: keep-alive\r\n\r\n')
        checknet_log.info('send %d bytes' % ret)
        #接收服务端消息
        data=sock.recv(256)
        checknet_log.info('recv %s bytes:' % len(data))
        checknet_log.info(data.decode())
        # 关闭连接
        sock.close()
    else:
        checknet_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
        if stagecode == 1:
            if subcode == 0:
                checknet_log.info('Please insert the SIM card.')
            else:
                checknet_log.info('The SIM card status is abnormal,Please confirm that the SIM card is available.')
        elif stagecode == 2:
            if subcode == -1:
                checknet_log.info('Get network state failed.')
            else:
                checknet_log.info('Failed to register network. ERRCODE={}'.format(subcode))
        elif stagecode == 3:
            if subcode == 0:
                checknet_log.info('Network dialing timeout.')

