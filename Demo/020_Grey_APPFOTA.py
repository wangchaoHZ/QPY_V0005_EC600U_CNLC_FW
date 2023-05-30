import app_fota
from misc import Power
import utime as time


files = ["0324_0331.bin"]
# files = ["Grey_SocketUART.py", "2.txt", "1.txt"]
# files_t = ["a_adcm.py", "a_channel.py", "a_main_start.py", "a_config.py", "data_node.py", "do.py", "file_db.py",
#            "hj212.py", "hmi.py", "lcd.py", "logging.py", "main.py", "modbus.py", "page_desk.py", "page_desk2.py",
#            "page_desk1.py", "page_history.py", "page_real.py", "page_tab.py", "pms.py", "pub_tool.py", "remoter.py",
#            "rx8010.py", "serial_port.py", "serial_ai.py", "service_mb_master.py", "service_pub.py", "sl651.py",
#            "smoker.py", "user_socket.py", "version.py"]
download_list = []
url = r'%s' % "http://alps.rivern.icu/kayden/"

for file in files:
    download_list.append({'url': (url + file), 'file_name': '/usr/%s' % file})
    # {'url': 'http://192.168.1.1:8002/file/download/JUY_X12_TC12_LX/Juy_ADC_detech.mpy','file_name': '/usr/Juy_ADC_detech.mpy'}

if download_list:
    print("downlist: %d\r\n" % len(download_list), download_list)
    fota = app_fota.new()
    result = fota.bulk_download(download_list)  # '/usr/q1'为绝对路径
    fota.set_update_flag()

    print("update ....", result)
    time.sleep(1)
    Power.powerRestart()  # 重启模块
