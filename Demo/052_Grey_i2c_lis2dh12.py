import log
import utime
import _thread
from machine import I2C
from machine import Pin

# 寄存器地址
LIS2DH12_OUT_X_L = 0x28
LIS2DH12_OUT_X_H = 0x29
LIS2DH12_OUT_Y_L = 0x2A
LIS2DH12_OUT_Y_H = 0x2B
LIS2DH12_OUT_Z_L = 0x2C
LIS2DH12_OUT_Z_H = 0x2D
LIS2DH12_FIFO_CTRL_REG = 0x2E

# 控制寄存器
LIS2DH12_CTRL_REG1 = 0x20
LIS2DH12_CTRL_REG2 = 0x21
LIS2DH12_CTRL_REG3 = 0x22
LIS2DH12_CTRL_REG4 = 0x23
LIS2DH12_CTRL_REG5 = 0x24
LIS2DH12_CTRL_REG6 = 0x25
LIS2DH12_REFERENCE_REG = 0x26
LIS2DH12_STATUS_REG = 0x27

# 状态寄存器
LIS2DH12_STATUS_REG_AUX = 0x7

# 中断寄存器
LIS2DH12_INT1_CFG = 0x30
LIS2DH12_INT1_SRC = 0x31
LIS2DH12_INT1_THS = 0x32
LIS2DH12_INT1_DURATION = 0x33

# 身份寄存器
LIS2DH12_WHO_AM_I = 0x0F

# 单击有关的寄存器
LIS2DH12_CLICK_CFG = 0x38
LIS2DH12_CLICK_SRC = 0x39
LIS2DH12_CLICK_THS = 0x3A
LIS2DH12_TIME_LIMIT = 0x3B
LIS2DH12_TIME_LATENCY = 0x3C


# 将其和外部的中断引脚绑定到一起。
class lis2dh12(object):
    i2c_dev = None
    address = None
    int_pin = None
    dev_log = None

    def init(self, slave_address):
        self.dev_log = log.getLogger("I2C")
        self.address = slave_address
        self.i2c_dev = I2C(I2C.I2C1, I2C.STANDARD_MODE)
        self.int_pin = Pin(Pin.GPIO14, Pin.IN, Pin.PULL_PU, 0)  # 中断引脚, 根据硬件连接不同而改变
        self.sensor_init()
        self.single_tap_enable()  # 配置单击检测
        self.start_sensor()
        pass

    def read_data(self, regaddr, datalen, debug=True):
        r_data = [0x00 for _ in range(datalen)]
        r_data = bytearray(r_data)
        reg_addres = bytearray([regaddr])
        self.i2c_dev.read(self.address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        if debug is True:
            self.dev_log.debug(" read 0x{0:02x} from 0x{1:02x}".format(ret_data[0], regaddr))
        return ret_data

    def write_data(self, regaddr, data, debug=True):

        # 新式处理方式
        reg = bytearray([regaddr])
        w_data = bytearray([data])
        # 临时将需要传送的地址放在数据位
        self.i2c_dev.write(self.address, reg, len(reg), w_data, len(w_data))

        # 老式处理方式
        # w_data = bytearray([regaddr, data])
        # # 临时将需要传送的地址放在数据位
        # self.i2c_dev.write(self.address, bytearray(0x00), 0, bytearray(w_data), len(w_data))

        if debug is True:
            self.dev_log.debug(" write 0x{0:02x} to 0x{1:02x}".format(data, regaddr))

    def sensor_reset(self):
        # 重置chip
        self.write_data(LIS2DH12_CTRL_REG5, 0x80)
        utime.sleep_ms(100)
        r_data = self.read_data(LIS2DH12_WHO_AM_I, 1)
        # 确定重启成功
        while r_data[0] != 0x33:
            r_data = self.read_data(LIS2DH12_WHO_AM_I, 1)
            utime.sleep_ms(5)
        self.dev_log.debug("传感器重置成功")
        pass

    def sensor_init(self):
        self.sensor_reset()  # 1. 重置设备
        # 2. 初始化传感器
        self.write_data(LIS2DH12_CTRL_REG2, 0x04)  # 使能高分辨率
        self.write_data(LIS2DH12_CTRL_REG3, 0x80)  # 将中断引到INT1 引脚上面， 默认高电平有效
        self.write_data(LIS2DH12_CTRL_REG4, 0x08)  # ±2g， High-resolution mode

    def single_tap_enable(self):
        self.write_data(LIS2DH12_CLICK_CFG, 0x15)  # 使能 XYZ 三轴单击中断，
        # self.write_data(LIS2DH12_CLICK_CFG, 0x10)  # 使能 Z 轴单击中断，
        self.write_data(LIS2DH12_CLICK_THS, 0x30)  # 设置阈值
        self.write_data(LIS2DH12_TIME_LIMIT, 0x18)  # 设置时间窗口限制
        self.write_data(LIS2DH12_TIME_LATENCY, 0x02)  # 设置延时

    def start_sensor(self):
        self.write_data(LIS2DH12_CTRL_REG1, 0x77)  # 设置ODR 400HZ ,enable XYZ.
        # self.write_data(LIS2DH12_CTRL_REG1, 0x74)  # 设置ODR ,enable Z轴.
        utime.sleep_ms(20)  # (7/ODR) = 18ms

    def read_xyz(self):
        data = []
        for i in range(6):
            r_data = self.read_data(LIS2DH12_OUT_X_L + i, 1)
            data.append(r_data[0])
        return data

    def processing_data(self):
        data = self.read_xyz()
        self.dev_log.info("xL:{:0>3d},xH:{:0>3d},yL:{:0>3d},yH:{:0>3d},zL:{:0>3d},zH:{:0>3d}".
                          format(data[0], data[1], data[2], data[3], data[4], data[5]))
        self.dev_log.info("X:{:0>3d}  Y:{:0>3d}  Z:{:0>3d}".
                          format((data[0] & data[1]), (data[2] & data[3]), (data[4] & data[5])))
        pass

    def exti_processing_data(self):
        value = self.int_pin.read()
        if value == 1:  # 检测到中断信号了
            self.processing_data()
            return 1
        else:
            return 0


# 参数说明
# state: 是否使能中断读取. 1:使能; 0:不使能
# delay: 延时时间(ms), 此参数在中断模式下无效
# retryCount: 读取次数
def is2dh12_thread(state, delay, retryCount):
    # | 参数      | 参数类型 | 说明                |
    # | -------- | ------- | ------------------ |
    # | CRITICAL | 常量     | 日志记录级别的数值 50 |
    # | ERROR    | 常量     | 日志记录级别的数值 40 |
    # | WARNING  | 常量     | 日志记录级别的数值 30 |
    # | INFO     | 常量     | 日志记录级别的数值 20 |
    # | DEBUG    | 常量     | 日志记录级别的数值 10 |
    # | NOTSET   | 常量     | 日志记录级别的数值 0  |
    log.basicConfig(level=log.NOTSET)  # 设置日志输出级别
    dev = lis2dh12()
    dev.init(0x19)
    while True:
        if state == 1:
            if dev.exti_processing_data() == 1:
                retryCount -= 1
        elif state == 0:
            dev.processing_data()
            utime.sleep_ms(delay)
            retryCount -= 1
        if retryCount == 0:
            break
    print("检测结束退出")


if __name__ == "__main__":
    _thread.start_new_thread(is2dh12_thread, (0, 1000, 10))
