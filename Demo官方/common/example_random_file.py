'''
@Author: Baron
@Date: 2020-06-22
@LastEditTime: 2020-06-22 17:16:20
@Description: example for module urandom
@FilePath: example_urandom_file.py
'''
import urandom as random
import log
import utime

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Random_example"
PROJECT_VERSION = "1.0.0"

log.basicConfig(level=log.INFO)
random_log = log.getLogger("random")


if __name__ == '__main__':
    # urandom.randint(start, end)
    # 随机1 ~ 4之间
    num = random.randint(1, 4)
    random_log.info(num)

    # random between 0~1
    num = random.random()
    random_log.info(num)

    # urandom.unifrom(start, end)
    # 在开始和结束之间生成浮点数
    num = random.uniform(2, 4)
    random_log.info(num)

    # urandom.randrange(start, end, step)
    # 2-bit binary,the range is [00~11] (0~3)
    num = random.getrandbits(2)
    random_log.info(num)

    # 8-bit binary,the range is [0000 0000~1111 11111] (0~255)
    num = random.getrandbits(8)
    random_log.info(num)

    # urandom.randrange(start, end, step)
    # 从开始到结束随机生成递增的正整数
    num = random.randrange(2, 8, 2)
    random_log.info(num)

    # urandom.choice(obj)
    # 随机生成对象中元素的数量
    num = random.choice("QuecPython")
    random_log.info(num)
