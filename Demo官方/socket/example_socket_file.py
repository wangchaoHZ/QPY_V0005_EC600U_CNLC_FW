'''
@Author: Baron
@Date: 2020-04-24
@LastEditTime: 2020-04-26 09:56:08
@Description: example for module usocket
@FilePath: example_socket_file.py
'''
# 导入usocket模块
import usocket
import log
import utime
import checkNet

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Socket_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
socket_log = log.getLogger("SOCKET")

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        socket_log.info('Network connection successful!')

        # 创建一个socket实例
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        # 解析域名
        sockaddr = usocket.getaddrinfo('www.tongxinmao.com', 80)[0][-1]
        # 建立连接
        sock.connect(sockaddr)
        # 向服务端发送消息
        ret = sock.send(
            'GET /News HTTP/1.1\r\nHost: www.tongxinmao.com\r\nAccept-Encoding: deflate\r\nConnection: keep-alive\r\n\r\n')
        socket_log.info('send %d bytes' % ret)
        # 接收服务端消息
        data = sock.recv(256)
        socket_log.info('recv %s bytes:' % len(data))
        socket_log.info(data.decode())

        # 关闭连接
        sock.close()
    else:
        socket_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
