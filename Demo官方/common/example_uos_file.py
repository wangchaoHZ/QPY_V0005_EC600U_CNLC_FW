import uos
import log
import utime

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Uos_example"
PROJECT_VERSION = "1.0.0"


log.basicConfig(level=log.INFO)
uos_log = log.getLogger("Uos")


if __name__ == '__main__':
    # 文件操作
    # create a file
    # 创建一个文件操作句柄
    f = open('/usr/test.txt','w')

    # 写入文件
    f.write('hello quecpython!\n')
    f.write('123456789abcdefg!\n')

    # 关闭文件句柄
    f.close()

    # read a file
    f = open('/usr/test.txt', 'r')
    uos_log.info(f.readline())
    uos_log.info(f.readline())
    f.close()

    # 也可使用with方法
    with open('/usr/test.txt','w')as f:
        f.write("hello quecpython!\n")
