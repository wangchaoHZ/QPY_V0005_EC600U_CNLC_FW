# PWM使用示例

from misc import PWM
import utime


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_PWM_example"
PROJECT_VERSION = "1.0.0"


'''
*PWM号和引脚对应关系：
        注：EC100YCN平台，支持PWM0~PWM3，对应引脚如下：
        PWM0 – 引脚号19
        PWM1 – 引脚号18
        PWM2 – 引脚号23
        PWM3 – 引脚号22

        注：EC600S/EC600N平台，支持PWM0~PWM3，对应引脚如下：
        PWM0 – 引脚号52
        PWM1 – 引脚号53
        PWM2 – 引脚号70
        PWM3 – 引脚号69
        
        注：EC200U平台，支持PWM0，对应引脚如下：
        PWM0 – 引脚号135
        
        注：EC600UCN平台，支持PWM0，对应引脚如下：
        PWM0 – 引脚号70
API详细介绍：https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=pwm
'''
# EC600S/EC600N可以直接运行，开发板上的灯会闪烁
# EC200U和EC600U需要自行连接外设查看现象

if __name__ == '__main__':
    pwm = PWM(PWM.PWM0, PWM.ABOVE_MS, 100, 200)  # 初始化一个pwm对象
    pwm.open()  # 开启PWM输出
    utime.sleep(10)
    pwm.close()  # 关闭pwm输出
