# -*- coding:utf-8 -*-
# @Time    : 2020/9/15 15:10
# @Author  : 年少风狂!
# @File    : game_filename.py
# @Software: PyCharm
import os

path = r"F:\game"  # 存储APP的路径
p = 0
for x in os.listdir(path):
    p += 1
    new_name = f'new{p}.apk'
    olddir = os.path.join(path, x)
    path1 = r'F:\new_game'
    Newdir = os.path.join(path1, new_name)
    os.rename(olddir, Newdir)