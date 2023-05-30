# -*- coding: UTF-8 -*-
# Source: https://github.com/pycom/pycom-modbus/tree/master/uModbus (2018-07-16)
# 导入模块
import log
import utime
import ujson
import _thread
import checkNet
from machine import UART
import ubinascii as binascii


# 串口信息
_uartport = UART.UART2  # 串口
_baudrate = 57600  # 波特率
_databits = 8  # 数据位
_parity = 0  # 校验
_stopbit = 1  # 停止位
_flowctl = 0  # 流控


# 下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
# 在执行用户代码前，会先打印这两个变量的值。
PROJECT_NAME = "Grey_Test"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# | Parameter | parameter | description               | type     |
# | --------- | --------- | ------------------------- | -------- |
# | CRITICAL  | constant  | value of logging level 50 | critical |
# | ERROR     | constant  | value of logging level 40 | error    |
# | WARNING   | constant  | value of logging level 30 | warning  |
# | INFO      | constant  | value of logging level 20 | info     |
# | DEBUG     | constant  | value of logging level 10 | debug    |
# | NOTSET    | constant  | value of logging level 0  | notset   |

# | 参数      | 参数类型 | 说明                | 类型      |
# | -------- | ------- | ------------------ | -------- |
# | CRITICAL | 常量     | 日志记录级别的数值 50 | critical |
# | ERROR    | 常量     | 日志记录级别的数值 40 | error    |
# | WARNING  | 常量     | 日志记录级别的数值 30 | warning  |
# | INFO     | 常量     | 日志记录级别的数值 20 | info     |
# | DEBUG    | 常量     | 日志记录级别的数值 10 | debug    |
# | NOTSET   | 常量     | 日志记录级别的数值 0  | notset   |
log.basicConfig(level=log.NOTSET)   # 设置日志输出级别
Grey_log = log.getLogger("Grey")


# 功能码
READ_COILS = 0x01  # 读线圈
READ_DISCRETE_INPUTS = 0x02  # 读离散量输入
READ_HOLDING_REGISTERS = 0x03  # 读保持寄存器
READ_INPUT_REGISTER = 0x04  # 读输入寄存器
WRITE_SINGLE_COIL = 0x05  # 写单个线圈
WRITE_SINGLE_REGISTER = 0x06  # 写单个寄存器
READ_EXCEPTION_STATUS = 0x07  # 读取异常状态
DIAGNOSTICS = 0x08  # 诊断
GET_COM_EVENT_COUNTER = 0x0B  # 获取com事件计数器
GET_COM_EVENT_LOG = 0x0C  # 获取com事件LOG
WRITE_MULTIPLE_COILS = 0x0F  # 写多个线圈
WRITE_MULTIPLE_REGISTERS = 0x10  # 写多个寄存器
REPORT_SERVER_ID = 0x11  # 报告服务器ID
READ_FILE_RECORD = 0x14  # 读文件记录
WRITE_FILE_RECORD = 0x15  # 写文件记录
MASK_WRITE_REGISTER = 0x16  # 屏蔽写寄存器
READ_WRITE_MULTIPLE_REGISTERS = 0x17  # 读/写多个寄存器
READ_FIFO_QUEUE = 0x18  # 读取FIFO队列
READ_DEVICE_IDENTIFICATION = 0x2B  # 读设备识别码

# 异常码
ILLEGAL_FUNCTION = 0x01  # 非法功能
ILLEGAL_DATA_ADDRESS = 0x02  # 非法数据地址
ILLEGAL_DATA_VALUE = 0x03  # 非法数据值
SERVER_DEVICE_FAILURE = 0x04  # 从站设备故障
ACKNOWLEDGE = 0x05  # 确认
SERVER_DEVICE_BUSY = 0x06  # 从属设备忙
MEMORY_PARITY_ERROR = 0x08  # 存储奇偶性差错
GATEWAY_PATH_UNAVAILABLE = 0x0A  # 不可用网关路径
DEVICE_FAILED_TO_RESPOND = 0x0B  # 网关目标设备响应失败

# PDU 常量表
CRC_LENGTH = 0x02  # CRC长度
ERROR_BIAS = 0x80  # 错误基数
RESPONSE_HDR_LENGTH = 0x02  # 响应HDR长度
ERROR_RESP_LEN = 0x05  # 错误注册长度
FIXED_RESP_LEN = 0x08  # 固定注册长度
MBAP_HDR_LENGTH = 0x07  # HDR包头长度

CRC16_TABLE = (
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241, 0xC601,
    0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440, 0xCC01, 0x0CC0,
    0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40, 0x0A00, 0xCAC1, 0xCB81,
    0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841, 0xD801, 0x18C0, 0x1980, 0xD941,
    0x1B00, 0xDBC1, 0xDA81, 0x1A40, 0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01,
    0x1DC0, 0x1C80, 0xDC41, 0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0,
    0x1680, 0xD641, 0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081,
    0x1040, 0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441, 0x3C00,
    0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41, 0xFA01, 0x3AC0,
    0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840, 0x2800, 0xE8C1, 0xE981,
    0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41, 0xEE01, 0x2EC0, 0x2F80, 0xEF41,
    0x2D00, 0xEDC1, 0xEC81, 0x2C40, 0xE401, 0x24C0, 0x2580, 0xE541, 0x2700,
    0xE7C1, 0xE681, 0x2640, 0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0,
    0x2080, 0xE041, 0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281,
    0x6240, 0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41, 0xAA01,
    0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840, 0x7800, 0xB8C1,
    0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41, 0xBE01, 0x7EC0, 0x7F80,
    0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40, 0xB401, 0x74C0, 0x7580, 0xB541,
    0x7700, 0xB7C1, 0xB681, 0x7640, 0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101,
    0x71C0, 0x7080, 0xB041, 0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0,
    0x5280, 0x9241, 0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481,
    0x5440, 0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841, 0x8801,
    0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40, 0x4E00, 0x8EC1,
    0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41, 0x4400, 0x84C1, 0x8581,
    0x4540, 0x8701, 0x47C0, 0x4680, 0x8641, 0x8201, 0x42C0, 0x4380, 0x8341,
    0x4100, 0x81C1, 0x8081, 0x4040
)


# # 生成CRC-16查找表的代码:
# def generate_crc16_table():
#     crc_table = []
#     print(crc_table, '\r\n')
#     for byte in range(256):
#         crc = 0x0000
#         for _ in range(8):
#             if (byte ^ crc) & 0x0001:
#                 crc = (crc >> 1) ^ 0xa001
#             else:
#                 crc >>= 1
#             byte >>= 1
#         crc_table.append(crc)
#     return crc_table
#
#
# def light_data_transfer(ret_str):
#     str_list = list(map(lambda x: x.decode("utf-8"), ret_str.split(b",")))
#     data_bits = int(str_list[2])
#     data_list = str_list[3: 3+data_bits]
#     one_place = int("0x" + data_list[0] + data_list[1], 16)
#     tens_place = int("0x" + data_list[2] + data_list[3], 16)
#     return tens_place * 10 + one_place


class ModbusInit:
    def __init__(self, uartport, baudrate, databits, parity, stopbit, flowctl, rt_pin):
        self.uart = UART(uartport, baudrate, databits, parity, stopbit, flowctl)
        self.uart.control_485(rt_pin, 1)

    @staticmethod
    def divmod_low_high(addr):  # 分离高低字节
        high, low = divmod(addr, 0x100)
        # Grey_log.debug("addr:0x{:04X}  high:0x{:02X}  low:0x{:02X}".format(addr, high, low))
        return high, low

    def calc_crc(self, string_byte):  # 生成CRC
        crc = 0xFFFF
        for pos in string_byte:
            crc ^= pos
            for i in range(8):
                if (crc & 1) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        gen_crc = hex(((crc & 0xff) << 8) + (crc >> 8))
        int_crc = int(gen_crc, 16)
        return self.divmod_low_high(int_crc)

    @staticmethod
    def split_return_bytes(ret_bytes):  # 转换二进制
        ret_str = binascii.hexlify(ret_bytes, ',')  # 二进制转字符串, 以','分隔.
        return ret_str.split(b",")  # 转换为列表, 以','分隔.

    def read_uart(self):  # UART接收
        num = self.uart.any()
        msg = self.uart.read(num)
        # Grey_log.debug('UART接收数据: ')
        # for i in range(num):
        #     Grey_log.debug('0x{:02X}'.format(msg[i]))
        # ret_str = binascii.hexlify(msg, ',')  # 二进制转字符串, 以','分隔.
        ret_str = self.split_return_bytes(msg)
        Grey_log.debug('UART接收数据: {}'.format(ret_str))
        return ret_str

    def write_coils(self, slave, const, start, coil_qty):  # UART发送
        start_h, start_l = self.divmod_low_high(start)
        coil_qty_h, coil_qty_l = self.divmod_low_high(coil_qty)
        data = bytearray([slave, const, start_h, start_l, coil_qty_h, coil_qty_l])
        # Grey_log.debug(data)
        crc = self.calc_crc(data)
        # Grey_log.debug("crc_high:0x{:02X}  crc_low:0x{:02X}".format(crc[0], crc[1]))
        for num in crc:
            data.append(num)
        self.uart.write(data)
        # Grey_log.debug('UART发送数据: ')
        # dataLen = len(data)
        # for i in range(dataLen):
        #     Grey_log.debug('0x{:02X}'.format(data[i]))
        ret_str = self.split_return_bytes(data)
        Grey_log.debug('UART发送数据: {}'.format(ret_str))
        return True


if __name__ == '__main__':
    # 手动运行本例程时, 可以去掉该延时, 如果将例程文件名改为main.py, 希望开机自动运行时, 需要加上该延时.
    # utime.sleep(5)
    # CDC口打印poweron_print_once()信息, 注释则无法从CDC口看到下面的poweron_print_once()中打印的信息.
    checknet.poweron_print_once()

    # 如果用户程序包含网络相关代码必须执行wait_network_connected()等待网络就绪(拨号成功).
    # 如果是网络无关代码, 可以屏蔽 wait_network_connected().
    # 注: 未插入SIM卡时函数不会阻塞.
    stagecode, subcode = checknet.wait_network_connected(120)
    Grey_log.debug('stagecode: {}   subcode: {}'.format(stagecode, subcode))
    # 网络已就绪: stagecode = 3, subcode = 1
    # 没插sim卡: stagecode = 1, subcode = 0
    # sim卡被锁: stagecode = 1, subcode = 2
    # 超时未注网: stagecode = 2, subcode = 0
    if stagecode != 3 or subcode != 1:
        Grey_log.warning('【Look Out】 Network Not Available\r\n')
    else:
        Grey_log.error('【Look Out】 Network Ready\r\n')

    Grey_log.info('User Code Start\r\n\r\n')

    modbus = ModbusInit(_uartport, _baudrate, _databits, _parity, _stopbit, _flowctl, UART.GPIO38)
    while True:
        if modbus.write_coils(0x01, READ_HOLDING_REGISTERS, 0X0003, 0x0002):
            retstr = modbus.read_uart()
            Grey_log.info(retstr)
        utime.sleep_ms(5000)

    # Grey_log.info('User Code End\r\n\r\n')
