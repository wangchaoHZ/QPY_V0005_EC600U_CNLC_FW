'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module ujson
@FilePath: example_json_file.py
'''

# ujson.loads 用于解码 JSON 数据。该函数返回 Python 字段的数据类型。

import ujson
import log
import utime


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_Json_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.INFO)
ujson_log = log.getLogger("UJSON loads")


if __name__ == '__main__':
    inp = {'bar': ('baz', None, 1, 2)}
    ujson_log.info(type(inp))
    # <class 'dict'>

    # 将Dict转换为json
    s = ujson.dumps(inp)
    ujson_log.info(s)
    ujson_log.info(type(s))
    # {"bar": ["baz", null, 1, 2]}, <class 'str'>

    # 将json转换为Dict
    outp = ujson.loads(s)
    ujson_log.info(outp)
    ujson_log.info(type(outp))
    # ujson.dump()和juson.load()主要用来读写json文件
