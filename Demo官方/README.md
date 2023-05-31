## 1. example文件目录说明



| 序号 | 文件名                                     | 功能                             | 备注                                                         |
| ---- | :----------------------------------------- | -------------------------------- | ------------------------------------------------------------ |
| 1    | aliyun/example_aliyun_file.py              | 阿里云物联网连接套件             | 使用前确认SIM注网成功                                        |
| 2    | common/example_math_file.py                | 数学运算math方法                 | 参考示例使用，可直接运行测试                                 |
| 3    | common/example_random_file.py              | 生成随机数                       | 参考示例使用，可直接运行测试                                 |
| 4    | common/example_string_file.py              | 字符串方法介绍                   | 参考示例使用，可直接运行测试                                 |
| 5    | common/example_uos_file.py                 | 文件操作                         | 示例运行后会创建txt文件                                      |
| 6    | dataCall/example_dataCall_callback_file.py | 设置网络状态变化后触发回调通知   | 示例会设置SIM为飞行模式后恢复                                |
| 7    | fota/example_fota_file.py                  | Fota升级                         | 需先提供升级包                                               |
| 8    | gpio/example_pin_file.py                   | gpio输出                         | 参考示例使用                                                 |
| 9    | http/example_request_get_file.py           | HTTP GET方法                     | 参考示例使用，可直接运行测试                                 |
| 10   | http/example_request_post_file.py          | HTTP POST方法                    | 参考示例使用，可直接运行测试                                 |
| 11   | http/example_request_ssl_file.py           | SSL                              | 参考示例使用，可直接运行测试                                 |
| 12   | I2C/example_i2c_file.py                    | I2C通信                          | 参考示例使用                                                 |
| 13   | json/example_json_file.py                  | json数据处理                     | 参考示例使用，可直接运行测试                                 |
| 14   | log/example_log_critical_file.py           | critical级别log输出              | 参考示例使用，可直接运行测试                                 |
| 15   | log/example_log_debug_file.py              | debug级别log输出                 | 参考示例使用，可直接运行测试                                 |
| 16   | log/example_log_error_file.py              | error级别log输出                 | 参考示例使用，可直接运行测试                                 |
| 17   | log/example_log_info_file.py               | info级别log输出                  | 参考示例使用，可直接运行测试                                 |
| 18   | log/example_log_warning_file.py            | warning级别log输出               | 参考示例使用，可直接运行测试                                 |
| 19   | mqtt/example_mqtt_file.py                  | MQTT客户端功能                   | 参考示例使用，可直接运行测试                                 |
| 20   | ntp/example_ntptime_file.py                | ntp时间同步                      | 参考示例使用，可直接运行测试                                 |
| 21   | pwm/example_pwm_file.py                    | pwm输出                          | 参考示例使用                                                 |
| 22   | socket/example_socket_file.py              | SOCKET连接                       | 参考示例使用，可直接运行测试                                 |
| 23   | TenCentyun/example_tencentyun_file.py      | 腾讯云物联网连接                 | 参考示例使用，配置腾讯云设备参数                             |
| 24   | thread/example_thread_file.py              | 多线程                           | 参考示例使用，可直接运行测试                                 |
| 25   | timer/example_timer_file.py                | 定时器                           | 参考示例使用，可直接运行测试                                 |
| 26   | tts/example_tts_file.py                    | TTS语音播报                      | 参考示例使用，可直接运行测试                                 |
| 27   | uart/example_uart_file.py                  | UART串口通信                     | 参考示例使用                                                 |
| 28   | utime/example_utime_localtime_file.py      | 获取本地时间                     | 参考示例使用，可直接运行测试                                 |
| 29   | utime/example_utime_mktime_file.py         | 获取当前时间戳                   | 参考示例使用，可直接运行测试                                 |
| 30   | utime/example_utime_sleep_file.py          | 休眠                             | 参考示例使用，可直接运行测试                                 |
| 31   | wdt/example_wdt_file.py                    | 看门狗（软狗）                   | 参考示例使用，可直接运行测试                                 |
| 32   | audio/example_audio_file.py                | 播放音频文件                     | 参考示例使用                                                 |
| 33   | main/main.py                               | main.py模板                      | 用户应在此模板的基础上添加自己的代码                         |
| 34   | debug/debug.py                             | 系统运行时打印必要的参数和内容   | 输出的信息有：当前可用ram、rom、电池电压以及信号强度；用户可酌情加减。 |
| 35   | SPI/example_spi_file.py                    | SPI通信                          | 参考示例                                                     |
| 36   | checkNet/example_checknet_file.py          | 阻塞等待网络就绪，超时返回异常码 | 参考示例和官方文档中关于checkNet部分的描述。                 |
| 37   | helloworld/example_helloworld_file.py      | QuecPython入门示例代码           | 直接下载运行                                                 |
| 38   | LED/example_LED_file.py                    | 点灯示例代码                     | 默认EC600S/N直接运行灯闪烁，其他模组更改屏蔽代码区域即可     |

