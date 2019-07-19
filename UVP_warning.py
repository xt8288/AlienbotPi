#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# 锂电池电压过低，报警程序
# 如果电池过放，输出端会没有电压输出，需要重新激活！！请联系售后

import tkinter
import time
import config_serial_servo
import pigpio
import os
import threading

vin_list = []

LED1 = 24

pi = pigpio.pi()
pi.set_mode(LED1, pigpio.OUTPUT)    # 将IO口设为输出


# 获取平均数
def get_average(num_list):
    num_sum = 0
    for item in num_list:
        num_sum += item
    return num_sum/len(num_list)


def led_flicker():
    global LED1
    while True:
        pi.write(LED1, 1)
        time.sleep(0.05)
        pi.write(LED1, 0)
        time.sleep(0.05)


while True:
    vin_list.append(config_serial_servo.serial_servo_read_vin(1))   # 读取舵机ID1的电压
    if len(vin_list) >= 10:
        #print (get_average(vin_list))
        if get_average(vin_list) < 6600:    # 舵机1在11秒内的平均电压 小于 6.8V
            os.system("sudo systemctl stop Hand_Service.service")  # 关闭舵机服务器
            threading.Thread(target=led_flicker).start()    # LED1,2快速闪烁
            vin_ok = False
            warn = tkinter.Tk()
            label_text = tkinter.Label(warn, fg='red', text='警告！电池电压过低，请断电充电！', font=('', 40))
            label_text.pack()
            # 进入消息循环
            warn.mainloop()
        vin_list = []
    time.sleep(1)
