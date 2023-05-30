import sms
import utime
import log 

# | 参数      | 参数类型 | 说明                |
# | -------- | ------- | ------------------ |
# | CRITICAL | 常量     | 日志记录级别的数值 50 |
# | ERROR    | 常量     | 日志记录级别的数值 40 |
# | WARNING  | 常量     | 日志记录级别的数值 30 |
# | INFO     | 常量     | 日志记录级别的数值 20 |
# | DEBUG    | 常量     | 日志记录级别的数值 10 |
# | NOTSET   | 常量     | 日志记录级别的数值 0  |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")

sms_num = 20
delete_flag = 0  # delete_flag；是否删除短信的标志位
pdu_decode_flag = 1  # pdu_decode_flag；是否PDU解析短信的标志位
while sms_num and delete_flag:
    if sms.searchTextMsg(sms_num-1) != -1:
        Grey_log.debug("删除 第{}条信息".format(sms_num-1))
        utime.sleep(1)
        sms_num -= 1
    else:
        Grey_log.debug("此index无消息，故不删除")
        utime.sleep(1)
        sms_num -= 1


while sms_num and pdu_decode_flag:
    if sms.searchTextMsg(sms_num-1) != -1:
        Grey_log.debug("PDU DECODE 第{}条信息".format(sms_num-1))
        sms_content = sms.decodePdu(sms.searchPduMsg(sms_num-1), sms.getPduLength(sms.searchPduMsg(sms_num-1)))
        print(sms_content)  
        utime.sleep(1)
        sms_num -= 1
    else:
        Grey_log.debug("此index无消息，故不解析")
        utime.sleep(1)
        sms_num -= 1
