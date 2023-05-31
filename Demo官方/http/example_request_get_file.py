import request
import log
import utime
import checkNet


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Requect_get_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
http_log = log.getLogger("HTTP GET")

url = "http://httpbin.org/get"

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        http_log.info('Network connection successful!')
        response = request.get(url)   # 发起http GET请求
        http_log.info(response.json())  # 以json方式读取返回
    else:
        http_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))