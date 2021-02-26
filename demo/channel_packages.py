# -*- coding:utf-8 -*-
# @Time    : 2020/8/13 19:12
# @Author  : 年少风狂!
# @File    : channel_packages.py
# @Software: PyCharm
import os


def adbcmdapk(filepath):  # 获取APK包名
    if not os.path.exists(filepath):  # 判断路径是否存在
        return 0
    # cmd控制台上过滤包名的命令
    package_activity = 'aapt dump badging %s |findstr "package launchable-activity"' % filepath
    result = os.popen(package_activity).readlines()  # 读取cmd控制台的信息命令并获取包名信息
    package_and_activity = list()
    for i in range(len(result)):
        if "package" in result[i]:
            name_number = result[i].find("e='")
            version_code_number = result[i].find("' v")
            package = result[i][name_number + 3:version_code_number]  # 获取包名
            package_and_activity.append(package)
        if "launchable-activity" in result[i]:
            name_number = result[i].find("e='")
            version_code_number = result[i].find("'  l")
            activity = result[i][name_number + 3:version_code_number]  # 获取启动名
            package_and_activity.append(activity)

    return package_and_activity[0]


path = r"F:\3.7.7packagerversion"  # 存储APP的路径
p = 0
for x in os.listdir(path):
    p += 1
    channel = x.split('_')[1]  # 获取渠道号
    # channel = x.split('.')[0]
    path_pa = path + '\\' + x  # 获取相应包位置的路径
    a = adbcmdapk(path_pa)
    if a != "com.zhangkongapp.joke.bamenshenqi":
        print(f'{channel}渠道包对应的包名是：{a}')
