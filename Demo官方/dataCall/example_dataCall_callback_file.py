import dataCall
import net
import utime
import checkNet

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_DataCall_example"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

state = 1
'''
dataCall.setCallback()
用户回调函数，当网络状态发生变化，比如断线、上线时，会通过该回调函数通知用户。
'''


# 定义回调函数
def nw_cb(args):
    global state
    pdp = args[0]  # pdp索引
    nw_sta = args[1]  # 网络连接状态 0未连接， 1已连接
    if nw_sta == 1:
        print("*** network %d connected! ***" % pdp)
    else:
        print("*** network %d not connected! ***" % pdp)
    state -= 1


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        print('Network connection successful!')
        # 注册回调函数
        dataCall.setCallback(nw_cb)

        # 进入飞行模式模拟触发
        net.setModemFun(4)
        utime.sleep(2)

        # 退出飞行模式再次模拟触发回调
        net.setModemFun(1)

        while 1:
            if state:
                utime.sleep(1)  # 加个延时避免EC200U/EC600U运行重启
                pass
            else:
                break
    else:
        print('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
