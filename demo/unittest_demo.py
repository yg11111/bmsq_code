# -*- coding:utf-8 -*-
# @Time : 2020-07-12 10:38 
# @Author : 年少轻狂
# @File : unittest_demo.py
# @Software: PyCharm

import unittest
import warnings
from appium import  webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction


class MyTestcase(unittest.TestCase):
	# 用例的初始化
	def setUp(self) -> None:  # 启动app
		# warnings.simplefilter("ignore", ResourceWarning)  # 忽略ResourceWarning类型的警告
		# desired_caps = dict()
		# desired_caps["platformName"] = "Android"
		# desired_caps["platformVersion"] = "10"		# desired_caps["deviceName"] = "xiaomi mix 2s"
		# desired_caps["appPackage"] = "com.zhangkongapp.joke.bamenshenqi"
		# desired_caps[""]
		print("setup")

	# 类的初始化
	@classmethod
	def setUpClass(cls) -> None:
		print("setupclass")

	def test_case1(self):
		print("case1")

	def test_case2(self,):
		print("case2")

	# 类的释放
	@classmethod
	def tearDownClass(cls) -> None:
		print("tearDownclass")

	# 用例的释放
	def tearDown(self) -> None:  # 退出app
		print("tearDown")


if __name__ == '__main__':
	unittest.main()