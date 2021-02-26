# -*- coding:utf-8 -*-
# @Time : 2020/7/9 12:47
# @Author: 年少轻狂
# @File : demo.py

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.connectiontype import ConnectionType
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl
import os

desired_caps = {
    "platformName": "Android",
    "platformVersion": "10",  # 可以写小版本也可以不写
    "deviceName": "xiaomi mix 2s",  # 设备名，安卓手机可以随意填写，ios手机必须真实
    "appPackage": "com.zhangkongapp.joke.bamenshenqi",
    "appActivity": "com.joke.bamenshenqi.mvp.ui.activity.LoadingActivity",
    "unicodeKeyboard": False,  # 支持中文输入，默认false  若使用全英文可以不填该参数
    "resetKeyboard": False,  # 重置输入法为系统默认,将键盘给隐藏起来
    "noReset": True,  # 不重新安装apk  不要重置app就是要恢复原始状态
    "noSign": True,  # 不重新签名apk
    "newCommandTimeout": 6000,  # 超时时间
    # "automationName": "UiAutomator2",
    #  如果测试的是混合应用并丏想直接进入WebView内容中， 那么需要设置这个capability的值为true
    # "autoWebview": True,
    "unid": "2550cbd9",  # 连接真机的唯一设备号
    "app": r'D:\packagerversion\app_baidu_VN3.7.7_VC3707011_2020-06-22_377_jiagu_sign.apk'
}
# 连接Appium Server，初始化自动化环境

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(3)  # 设置等待时间
driver.background_app(5)  # 进入后台等待5s后，再回到前台
driver.get_window_size()  # 获得手机屏幕分辨率，从而得到屏幕宽度和高度 返回一个字典
driver.get_screenshot_as_file("png1.png")  # 截图
print(driver.network_connection)  # 获取当前网络 返回0,1,2,4,6 0-没有卡 1-飞行模式，2-wifi, 4-网络，6,-WiFi和网络
driver.set_network_connection(2)  # 设置当前网络
if driver.network_connection == ConnectionType.DATA_ONLY:  # 判断当前网络是否是4G网络  #网络的类型建议使用系统提供的类型
    # from appium.webdriver.connectiontype import ConnectionType
    print(10)
# 长按按键
driver.long_press_keycode(self, keycode, metastate=None, flags=None)
# 发送键到设备
driver.press_keycode(66)  # 参数是按键对应编码，可以百度搜索按键对应的编码（Android keycode)
# 或者另一个语法
driver.press_keycode(AndroidKey.ENTER)
# 打开通知栏
driver.open_notifications()
# 关闭通知栏  方法1：直接系统返回键 方法2：模拟滑动操作
driver.press_keycode(AndroidKey.BACK)
driver.start_activity("packages", "activiy")  # 在该app中跳转或打开其他APP的方法
# 输出当前程序的包名和启动名或界面名
print(driver.current_package)
print(driver.current_activity)
driver.install_app("apk包路径")  # 安装app
driver.remove_app("packages")  # 卸载app
# 获取当前的activity
print(driver.current_activity)
driver.is_app_installed("package")  # 根据包名判断该应用是否安装
# 如果有隐私政策弹窗，点击“同意并继续”
iknow = driver.find_element_by_id("tv_confirm")
iknow.get_attribute("enables")   # 根据该元素的enables属性名获取属性值
# classs属性的属性名是className, resource_id属性的属性名是resourceId
print(iknow.location)  # 获取元素的位置  返回字典x坐标和Y坐标
print(iknow.size)  # 获取元素的大小  返回字典height高和width宽
# save_screenshot()直接保存当前屏幕截图到当前脚本所在文件位置
driver.save_screenshot('login.png')
# get_screenshot_as_file(self,filename)将截图保存到指定文件路径
driver.get_screenshot_as_file('./images/login.png')
if iknow:  # 判断用户是否第一次登录app
    iknow.click()
    driver.find_element(MobileBy.ID,
                        "com.lbe.security.miui:id/permission_allow_button_1"
                        ).click()
    # android_uiautomator方法根据id定位元素就调用resourceId
    driver.find_element_by_android_uiautomator(
        'new UiSelector().resourceId("com.lbe.security.miui:id/permission_allow_button_1")'
    ).click()
    # 或者另外一个语法， driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
    #                           'resourceId("com.lbe.security.miui:id/permission_allow_button_1")'
    #                           )
    # android_uiautomator方法根据accessibility_id定位元素就调用description
    # driver.find_element_by_android_uiautomator(
    #     'new UiSelector().description("java代码str需双引号")')
    driver.implicitly_wait(3)
    TouchAction(driver).tap(x=574, y=1497).perform()  # 多次点击可以使用count参数
    TouchAction(driver).tap(x=579, y=1478).perform()
    TouchAction(driver).press(2, 5).move_to()
    driver.find_element_by_xpath(
        "//*[@resource-id='com.zhangkongapp.joke.bamenshenqi:id/tabs_rg']/android.widget.RadioButton[5]"
    ).click()
    TouchAction(driver).tap(x=532, y=1945).perform()
driver.implicitly_wait(4)
els = driver.find_elements_by_class_name("android.widget.RadioButton")[4]
els.click()
driver.find_element_by_xpath("//android.widget.RadioButton[5]").click()
print(els.text)
print('gsdg')
driver.close_app()  # 关闭当前运行程序的app
driver.quit()  # 关闭driver驱动对象

# 元素等待
# 可能由于一些原因，我们想找的元素并没有立刻出来，此时如果直接定位会报错
# 1、由于网络速度原因 2、服务器处理请求原因 3、电脑配置原因
# 隐式等待  针对所有元素去找
driver.implicitly_wait(2)  # 未找到就NoSuchElementexception抛异常
# 显式等待  针对单个元素去寻找
wait = WebDriverWait(driver, 5, 1)   # timeout=5超时时间  poll_frequency=1,默认是0.5
# 在5秒钟内, 每1秒去调用下面的方法去查找需要的元素，未找到就timeoutexception抛异常
wait.until(lambda x: x.find_element_by_id("")).click()

print()