'''
@Author: Pawn
@Date: 2020-08-19
'''
import log
import utime

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_String_example"
PROJECT_VERSION = "1.0.0"

log.basicConfig(level=log.INFO)
str_log = log.getLogger("String")

# QuecPython-字符串处理函数示例说明

if __name__ == '__main__':
    # decode   指定的编码格式解码字符串,默认为UTF-8
    bytes_m = b"abc"
    str_log.info(type(bytes_m))
    # <class 'bytes'>
    str_m = bytes_m.decode()
    str_log.info(type(str_m))
    # <class 'str'>

    # encode   指定的编码格式编码字符串,默认为UTF-8
    str_m = "中文"
    bytes_m = str_m.encode('utf-8')
    str_log.info(bytes_m)
    str_log.info(type(bytes_m))
    # b'\xe4\xb8\xad\xe6\x96\x87' <class 'bytes'>

    # find() 检测字符串中是否包含子字符串
    # 如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1
    str1 = "this is string example....wow!!!"
    str2 = "exam"
    str_log.info(str1.find(str2))
    # 15
    str_log.info(str1.find(str2, 10))
    # 15
    str_log.info(str1.find(str2, 40))
    # -1

    # rfind() 返回字符串最后一次出现的位置(从右向左查询)，如果没有匹配项则返回-1
    str1 = "this is string example....wow!!!"
    substr = "is"
    str_log.info(str1.rfind(substr))
    # 5
    str_log.info(str1.rfind(substr, 0, 10))
    # 5
    str_log.info(str1.rfind(substr, 10, 0))
    # -1

    # index() 检测字符串中是否包含子字符串,该方法与find()方法一样，只不过如果str不在 string中会报一个异常
    str1 = "this is string example....wow!!!"
    str2 = "exam"
    str_log.info(str1.index(str2))
    # 15
    str_log.info(str1.index(str2, 10))
    # 15

    try:
        str_log.info(str1.index(str2, 40))
    except Exception as e:
        str_log.error(str(e))

    # ValueError: substring not found

    # rindex() 同index(),从右到左查询

    # join() 将序列中的元素以指定的字符连接生成一个新的字符串
    # str.join(sequence)  // sequence -- 要连接的元素序列
    ustr = "-"
    seq = ("a", "b", "c") # 字符串序列
    str_log.info(ustr.join(seq))
    # a-b-c

    # split() 通过指定分隔符对字符串进行切片,返回一个list
    # str.split(str="", num=string.count(str))
    # str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
    # num -- 分割次数。默认为 -1, 即分隔所有。
    ustr = "Line1-abcdef \nLine2-abc \nLine4-abcd"
    str_log.info(ustr.split( ))     # 以空格为分隔符，包含 \n
    # ['Line1-abcdef', 'Line2-abc', 'Line4-abcd']
    str_log.info(ustr.split(' ', 1)) # 以空格为分隔符，分隔1次
    # ['Line1-abcdef', '\nLine2-abc \nLine4-abcd']


    # rsplit() 同split(), 从右到左进行分割

    # startswith() 检查字符串是否是以指定子字符串开头
    # str.startswith(str, beg=0,end=len(string))
    # 如果是则返回 True，否则返回 False。可传入参数从指定位置开始
    ustr = "this is string example....wow!!!"
    str_log.info(ustr.startswith( 'this' ))
    # True
    str_log.info(ustr.startswith( 'is', 2))
    # True
    str_log.info(ustr.startswith( 'this', 2))
    # False

    # endswith() 用于判断字符串是否以指定后缀结尾
    ustr = "this is string example....wow!!!"
    str_log.info(ustr.endswith( 'wow'))
    # False
    str_log.info(ustr.endswith( "wow!!!"))
    # True

    # strip() 用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    # 该方法只能删除开头或是结尾的字符，不能删除中间部分的字符
    ustr = "00000003210Python01230000000"
    str_log.info(ustr.strip('0'))  # 去除首尾字符 0
    # 3210Python0123
    str2 = "   Python      "
    str_log.info(str2.strip())    # 去除首尾空格
    #  Python

    # lstrip() 同strip() ,用于截掉字符串左边的空格或指定字符

    # rstrip() 同strip() ,用于截掉字符串右边的空格或指定字符

    # format() 字符串格式化,类似 %s 占位符
    str_log.info("{} {}".format("hello", "world"))    # 不设置指定位置，按默认顺序
    # hello world
    str_log.info("{0} {1}".format("hello", "world"))  #  # 设置指定位置
    # hello world
    str_log.info("{start} {end}".format(start="hello", end="world"))  # k,v形式指定位置
    # hello world

    # replace() 把字符串中的 old（旧字符串）替换成 new(新字符串)，如果指定第三个参数max，则替换不超过max次
    # str.replace(old, new, max)
    ustr = "this is string example....wow!!! this is really string"
    str_log.info(ustr.replace("is", "was"))
    # thwas was string example....wow!!! thwas was really string
    str_log.info(ustr.replace("is", "was", 3))
    # thwas was string example....wow!!! thwas is really string

    # count()  统计字符串里某个字符出现的次数。可选参数为在字符串搜索的开始与结束位置
    # str.count(sub, start= 0,end=len(string))
    ustr = "this is string example....wow!!!"
    sub = "i"
    str_log.info("str.count(sub, 4, 40) : ")
    str_log.info(ustr.count(sub, 4, 40))
    # str.count(sub, 4, 40) :  2

    # lower() 转换字符串中所有大写字符为小写
    # str.lower()
    ustr = "THIS IS STRING EXAMPLE....WOW!!!"
    str_log.info(ustr.lower())
    # this is string example....wow!!!

    # upper() 转换字符串中所有小写字符为大写

    # isspace()  检测字符串是否只由空格组成
    # 如果字符串中只包含空格，则返回 True，否则返回 False.

    # isalpha()  检测字符串是否只由字母组成
    # 如果字符串中只包含空格，则返回 True，否则返回 False.

    # isdigit() 检测字符串是否只由数字组成
    # 如果字符串中只包含空格，则返回 True，否则返回 False.

    # isupper()  检测字符串中所有的字母是否都为大写
    # 如果字符串中只包含空格，则返回 True，否则返回 False.

    # islower()  检测字符串中所有的字母是否都为大写
    # 如果字符串中只包含空格，则返回 True，否则返回 False.





