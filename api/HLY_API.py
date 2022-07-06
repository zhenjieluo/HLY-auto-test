# /*
#  * @Author: luo zhenjie 
#  * @Date: 2022-06-29 10:23:51 
#  * @Last Modified by:   luo zhenjie 
#  * @Last Modified time: 2022-06-29 10:23:51 
#  */
import jsonpath
import serial
import re
import time
from api.IOT_CLOUD_API import IOT_CLOUD_API

cloud = IOT_CLOUD_API()
cloud.username = 'luozhenjie'
cloud.password = 'aa123456'
cloud.device_id = 'BllRQflFa1jvbcZE4DYA'


class HLY_API(object):

    def __init__(self):
        self.com = ''
        self.port = ''
        self.com1 = ''
        self.port1 = ''
        self.oh = ''

    def com_send(self, sendtext):  # 串口发送
        com = self.com
        port = self.port
        try:
            ser = serial.Serial(com, port)
        except:
            ser = serial.Serial(com, port)
        ser.write(sendtext.encode())
        ser.close()

    def com_send1(self, sendtext):  # 串口发送
        com1 = self.com1
        port1 = self.port1
        try:
            ser = serial.Serial(com1, port1)
        except:
            ser = serial.Serial(com1, port1)
        ser.write(sendtext.encode())
        ser.close()

    def com_read(self):  # 串口读取
        com = self.com
        port = self.port
        try:
            ser = serial.Serial(com, port)
        except:
            ser = serial.Serial(com, port)
        while True:
            readtext = ''
            while ser.in_waiting > 0:
                readtext = ser.read(ser.in_waiting).decode('latin1')  # 一个一个的读取
                return readtext

    @staticmethod
    def create_data(angle, mode, soh, oh, singal):
        data_list = []
        data = '%s,%s,%s,%s,%s,0253,' % (str(angle).zfill(4), str(mode).zfill(2), str(soh).zfill(4), str(oh).zfill(4),
                                         str(singal).zfill(4))

        for i in data:
            a = ord(i)
            data_list.append(a)

        if len(data) == 28:
            oh_data = ('*XD,' + data + str(sum(data_list))+'#')
            return oh_data

        elif len(data) > 28:
            data_real = data_list[:28]
            oh_data = ('*XD,' + data + str(sum(data_real))+'#')
            return oh_data

    def init_data(self, angle, mode, soh, oh, singal):
        while True:
            start_collect = re.search('sent done', self.com_read())
            if start_collect:
                print('正在模拟探头数据，液位高度设置为%s' % oh)
                for i in range(30):
                    self.com_send1(self.create_data(angle, mode, soh, oh, singal))
                    time.sleep(1)
                break
            else:
                continue

        while True:
            report_data = re.search('sendStr', self.com_read())
            if report_data:
                print('设备已进行主动上报')
                time.sleep(60)
                break
            else:
                continue

        while True:
            oh_data = jsonpath.jsonpath(cloud.get_device_detail(),
                                        '$...dataPoints[?(@.dataPointName == "OH" )].dataPointReportedValue')
            print(oh_data)
            if oh_data == [oh]:
                break
            else:
                continue
        print('油位高度已调整为%s' % oh)