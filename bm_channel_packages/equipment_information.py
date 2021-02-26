# -*- coding:utf-8 -*-
# @Time    : 2020/7/30 11:57
# @Author  : 年少风狂!
# @File    : equipment_information.py
# @Software: PyCharm
import os


class Equipment(object):
    def unid(self):  # 获取设备id(序列号)
        un_id = os.popen("adb shell getprop ro.serialno").readlines()
        return un_id[0].replace('\n', '')

    def system_version(self):  # 获取android系统版本
        system_version = os.popen('adb shell getprop ro.build.version.release').read()
        return system_version.replace("\n", '')

    def android_id(self):  # 获取android_id
        android_id = os.popen("adb shell settings get secure android_id").read()
        return android_id.replace("\n", '')

    def device_imei(self):  # 获取设备iemi
        # imei = os.popen("adb shell getprop gsm.baseband.imei").read()
        imei = os.popen("adb shell dumpsys iphonesubinfo").read()
        return imei

    def device_model(self):  # 获取手机型号
        device_model = os.popen("adb -d shell getprop ro.product.model").read()
        return device_model

    def handset_makers(self): # 获取手机厂商
        device_makers = os.popen("adb -d shell getprop ro.product.brand").read()
        return device_makers

    def handset_name(self):  # 获取手机名称
        makers = self.handset_makers()
        model = self.device_model()
        handset_name = makers.replace("\n", "") + " " + model.replace("\n", "")
        return handset_name

