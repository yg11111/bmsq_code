# -*- coding:utf-8 -*-
# @Time : 2020/7/13 12:50
# @Author: 年少轻狂(yg)
# @File : bmsq_packages.py
import os
import time
import random
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.extensions.android.nativekey import AndroidKey
from equipment_information import Equipment
from bm_background import BmSpiders


class Packages(object):
    def __init__(self):
        pass

    def adbcmdapk(self, filepath):  # 获取APK包名
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

        return package_and_activity

    def start_appium(self, package_and_activity, app_path):  # 连接Appium Server，初始化自动化环境
        desired_caps = dict()
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = Equipment().system_version()
        desired_caps["deviceName"] = Equipment().handset_name()
        desired_caps["automationName"] = "UiAutomator2"
        desired_caps["appPackage"] = package_and_activity[0]
        desired_caps["activity"] = package_and_activity[1]
        desired_caps["app"] = app_path
        desired_caps["unid"] = Equipment().unid()
        desired_caps["unicodeKeyboard"] = False
        desired_caps["resetKeyboard"] = False
        desired_caps["noReset"] = True
        desired_caps["noSign"] = True
        desired_caps["newCommandTimeout"] = 6000
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        return driver

    def one_install_login_sn(self, driver, channel, p):  # 判断用户是否首次安装该app以及登录状态、登录统计点上报
        time.sleep(4)
        if "同意并继续" in driver.page_source:  # 判断当前设备是否首次安装该app
            wait = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id('tv_confirm'))
            wait.click()
            # driver.find_element_by_id("tv_confirm").click()
            # driver.find_element_by_android_uiautomator(
            #     'new UiSelector().resourceId("com.lbe.security.miui:id/permission_allow_button_1")'
            # ).click()
            els1 = WebDriverWait(driver, 5, 1).until(
                lambda x: x.find_element_by_android_uiautomator('text("始终允许").className("android.widget.Button")')
            )
            els1.click()
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("始终允许").className("android.widget.Button")'
            ).click()
            wait_element = WebDriverWait(driver, 6, 1).until(
                lambda x: x.find_element_by_id('tag_0')
            )
            wait_element.click()
            # driver.find_element_by_id("tag_3")
            driver.find_element_by_android_uiautomator('text("首页").className("android.widget.RadioButton")').click()
            # self.little_game(driver, channel, p)
            driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                'resourceIdMatches(".*tag_3")'
                                ).click()
        # else:
        #     self.little_game(driver, channel, p)
        els1 = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id("tag_3"))
        els1.click()
        driver.find_element(MobileBy.ID, 'tag_3').click()
        if "未登录" in driver.page_source:  # 判断当前账号是否已登录
            driver.find_element(MobileBy.ID, "iv_head_icon").click()
            # driver.implicitly_wait(2)
            time.sleep(1)
            time_and_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 获取当前日期，方便查询登录SQL
            self.login_methods(driver, channel)
        else:
            element = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id("iv_setting"))
            element.click()
            # driver.find_element_by_android_uiautomator(
            #     'new UiSelector().resourceIdMatches(".*iv_setting")'
            # ).click()
            time.sleep(2)
            els2 = WebDriverWait(driver, 3, 1).until(
                lambda x: x.find_element_by_android_uiautomator('text("切换账号").className("android.widget.TextView")')
            )
            els2.click()
            # driver.find_element(
            #     MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("切换账号").className("android.widget.TextView")'
            # ).click()
            time_and_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.third_party_login(driver, channel)
            els3 = WebDriverWait(driver, 5, 1).until(
                lambda x: x.find_element_by_android_uiautomator('resourceIdMatches(".*id_ib_view_actionBar_back")')
            )
            els3.click()
        username = driver.find_element(MobileBy.ID, "tv_user_name").text

        return username, time_and_date

    def third_party_login(self, driver, channel):  # 测试第三方登录
        # try:
        #     driver.find_element_by_id('qq').click()
        #     time.sleep(2)
        #     if "设置账密" in driver.page_source:  # 判断当前账号登录QQ是否首次登录
        #         driver.find_element(MobileBy.ID, 'tv_right').click()
        #         driver.find_element(
        #             MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
        #         ).click()
        #     elif "QQ授权登录" in driver.page_source:
        #         # driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
        #         #                     'new UiSelector().resourceId("com.tencent.mobileqq:id/fds")'
        #         #                     ).click()
        #         element = WebDriverWait(driver, 3, 1).until(
        #             lambda x: x.find_element_by_id("com.tencent.mobileqq:id/fds")
        #         )
        #         element.click()
        #     else:
        #         pass
        #     toast_element = WebDriverWait(driver, 5, 1).until(
        #         lambda x: x.find_element_by_xpath("//android.widget.Toast")
        #     )
        #     if ("登录成功" not in toast_element.text) or ("授权成功" not in toast_element.text):
        #         print(toast_element.text)
        # except:
        #     print(f'{channel}渠道包qq登录异常')
        # els = WebDriverWait(driver, 5, 1).until(lambda  x: x.find_element_by_android_uiautomator(
        #     'text("切换账号").className("android.widget.TextView")'
        # ))
        # els.click()
        # # driver.find_element(
        # #     MobileBy.ANDROID_UIAUTOMATOR, 'text("切换账号").className("android.widget.TextView")'
        # # ).click()
        try:
            time.sleep(2)
            driver.find_element_by_id('weixin').click()
            toast_element = WebDriverWait(driver, 5, 1).until(
                lambda x: x.find_element_by_class_name("android.widget.Toast")
            )
            print(toast_element.text)
            if ("登录成功" not in toast_element.text) or ("授权成功" not in toast_element.text):
                if toast_element == "八门神器：授权成功":
                    pass
                else:
                    print(toast_element.text)
        except:
            print(f'{channel}渠道包微信登录异常')
        # driver.find_element(
        #     MobileBy.ANDROID_UIAUTOMATOR, 'text("切换账号").className("android.widget.TextView")'
        # ).click()
        # try:
        #     time.sleep(1)
        #     driver.find_element_by_id('weibo').click()
        #     time.sleep(3)
        #     toast_element = WebDriverWait(driver, 3, 1).until(
        #         lambda x: x.find_element_by_xpath("//android.widget.Toast")
        #     )
        #     if ("登录成功" not in toast_element.text) or ("授权成功" not in toast_element.text):
        #         print(toast_element.text)
        # except:
        #     print(f'{channel}渠道包微博登录异常')

    def login_methods(self, driver, channel):  # 本机号码一键登录以及第三方登录
        if "本机号码一键登录" in driver.page_source:  # 判断当前设备是否可以本机号码一键登录
            try:
                one_key_login = driver.find_element_by_android_uiautomator(
                    'resourceIdMatches(".*one_key_login")'
                )
                one_key_login.click()
                if "设置账密" in driver.page_source:  # 判断当前账号的本机号码是否首次登录
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                toast_loc = ("xpath", ".//android.widget.Toast")
                toast_element = WebDriverWait(driver, 3, 1).until(ec.presence_of_element_located(toast_loc))
                if "登录成功" not in toast_element.text:
                    print(toast_element.text)
            except:
                print(channel + "渠道包，登录异常")
                # 抛异常后，账密登录继续执行以下代码
                driver.find_element(MobileBy.ID, 'tv_check_code').click()
                self.relative_coordinates_element(driver, 347, 1178)
                # TouchAction(driver).tap(
                #     x=347, y=1178).perform()
                driver.find_element_by_id('id_TV_activity_registerByTel_useUsername').click()
                self.relative_coordinates_element(driver, 562, 1420)
                # TouchAction(driver).tap(x=562, y=1420).perform()
                driver.find_element(MobileBy.ID, 'id_tv_activity_oneKeyRegister_register').click()
                time.sleep(1.5)
                driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("我知道了").className("android.widget.TextView")'
                ).click()
        else:
            try:
                qq_element = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id('qq_login'))
                # qq = driver.find_element_by_id('qq_login')
                qq_element.click()
                if "设置账密" in driver.page_source:  # 判断当前账号登录QQ是否首次登录
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                elif "QQ授权登录" in driver.page_source:
                    # driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                    #                     'new UiSelector().resourceId("com.tencent.mobileqq:id/fds")'
                    #                     ).click()
                    element = WebDriverWait(driver, 3, 1).until(
                        lambda x: x.find_element_by_id("com.tencent.mobileqq:id/fds")
                    )
                    element.click()
                else:
                    pass
                toast_element = WebDriverWait(driver, 3, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if "登录成功" not in toast_element.text or "授权成功" not in toast_element.text:
                    print(toast_element.text)
            except:
                print(channel + "渠道包，登录异常")
                self.relative_coordinates_element(driver, 347, 1178)
                # TouchAction(driver).tap(x=347, y=1178).perform()
                driver.find_element_by_id(
                    'id_TV_activity_registerByTel_useUsername'
                ).click()
                self.relative_coordinates_element(driver, 562, 1420)
                # TouchAction(driver).tap(x=562, y=1420).perform()
                driver.find_element(MobileBy.ID, 'id_tv_activity_oneKeyRegister_register').click()
                time.sleep(1.5)
                driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("我知道了").className("android.widget.TextView")'
                ).click()

    def not_weChatUserName(self, driver, channel):
        if "未绑定" in driver.page_source:  # 判断当前账号是否已绑定微信
            try:
                driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*relative_weChat")'
                ).click()
                # 当前账号是首次绑定微信
                # driver.start_activity("com.tencent.mm", ".ui.LauncherUI")
                ele = WebDriverWait(driver, 4, 1).until(
                    lambda x: x.find_element_by_id("com.tencent.mm:id/br")
                )
                ele.click()
                # driver.find_element_by_android_uiautomator('resourceId("com.tencent.mm:id/br")').click()
                try:
                    toast_element = WebDriverWait(driver, 3, 1).until(
                        lambda x: x.find_element_by_xpath("//android.widget.Toast")
                    )
                    if "绑定失败" not in toast_element.text:
                        print(toast_element.text)
                except:
                    print(channel + "渠道包，绑定微信toast异常")
            except:
                print(channel + "渠道包，绑定微信异常")

    def weChatUserName(self, driver, channel):
        driver.find_element(
            MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageView").index(4)'
        ).click()
        # driver.find_element_by_id("iv_head_icon").click()
        self.not_weChatUserName(driver, channel)
        if "已绑定" in driver.page_source:
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("切换账号").className("android.widget.TextView")'
            ).click()
            if "账密登录" in driver.page_source:
                driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("账密登录").className("android.widget.TextView")'
                ).click()
            self.relative_coordinates_element(driver, 347, 1178)
            # TouchAction(driver).tap(x=347, y=1178).perform()
            driver.find_element_by_android_uiautomator(
                'text("用户名注册").className("android.widget.TextView")'
            ).click()
            self.relative_coordinates_element(driver, 562, 1420)
            # TouchAction(driver).tap(x=562, y=1420).perform()
            driver.find_element(MobileBy.ID, 'id_tv_activity_oneKeyRegister_register').click()
            time.sleep(2)
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("我知道了").className("android.widget.TextView")'
            ).click()
            self.not_weChatUserName(driver, channel)
        driver.find_element_by_class_name('android.widget.ImageButton').click()

    def pay_sn(self, driver, p, channel):  # 充值统计点上报
        driver.find_element(
            MobileBy.ID, "ll_container_bm_currency"
        ).click()
        wait = WebDriverWait(driver, 3, 1).until(
            lambda x: x.find_element_by_xpath('//android.widget.LinearLayout/android.widget.Button')
            )
        wait.click()
        # driver.find_element_by_xpath('//android.widget.LinearLayout/android.widget.Button').click()
        if "下次再说" in driver.page_source:  # 判断当前账号是否绑定手机号
            driver.find_element_by_id('tv_cancel').click()
        data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 拉起微信支付
        if p % 2 != 0:
            try:
                wx_pay = driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("微信支付").className("android.widget.TextView")'
                )
                wx_pay.click()
                time.sleep(2)
                els = WebDriverWait(driver, 5, 1).until(lambda x: x.find_element_by_id(
                                                        'com.tencent.mm:id/dn')
                                                        )
                els.click()
                # driver.find_element_by_id('com.tencent.mm:id/dn').click()
                element = WebDriverWait(driver, 3, 1).until(
                    lambda x: x.find_element_by_android_uiautomator(
                        'resourceId("com.tencent.mm:id/doz")'
                    ))
                element.click()
                # driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                #                     'resourceId("com.tencent.mm:id/doz")'
                #                     ).click()
            except:
                print(channel + "渠道包，充值异常")
        # 拉起支付宝支付
        else:
            try:
                zfb_pay = driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("支付宝").className("android.widget.TextView")'
                )
                zfb_pay.click()
                time.sleep(3)
                # driver.start_activity("com.eg.android.AlipayGphone",
                #                       "com.alipay.android.msp.ui.views.MspContainerActivity"
                #                       )
                wait = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_accessibility_id("退出"))
                wait.click()
                # driver.find_element_by_android_uiautomator('description("退出")').click()
                els1 = WebDriverWait(driver, 5, 1).until(lambda x: x.find_element_by_id(
                    "com.alipay.mobile.antui:id/cancel"
                ))
                els1.click()
                # driver.find_element(
                #     MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("放弃").className("android.widget.TextView")'
                # ).click()
            except:
                print(print(channel + "渠道包，充值异常"))
        if p % 2 == 0:
            element_wait = WebDriverWait(driver, 10, 1).until(
                lambda x: x.find_element_by_android_uiautomator(
                    'text("我没有支付").className("android.widget.Button").index(0)'
                ))
            # prompt_cancel = driver.find_element_by_xpath('//android.widget.LinearLayout/android.widget.Button[1]')
            element_wait.click()
            try:
                toast_loc = ("xpath", ".//android.widget.Toast")
                toast_element = WebDriverWait(driver, 5, 1).until(ec.presence_of_element_located(toast_loc))
                if '八门神器：支付失败' not in toast_element.text:
                    print(toast_element.text)
            except:
                print(channel + "渠道包，充值toast异常")

        else:
            prompt_ok_bt = WebDriverWait(driver, 10, 1).until(lambda x: x.find_element_by_android_uiautomator(
                'text("已支付").className("android.widget.Button")')
                                                    )
            # prompt_ok_bt = driver.find_element(
            #     MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("已支付").className("android.widget.Button")'
            # )
            prompt_ok_bt.click()
            try:
                toast_element = WebDriverWait(driver, 7, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if '交易失败，如有疑问，请联系客服' not in toast_element.text:
                    print(toast_element.text)
            except:
                print(channel + "渠道包，充值toast异常")

        return data

    def relative_coordinates_element(self, driver, coordinates_x, coordinates_y):
        # 获取当前手机的分辨率
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']
        # 假设当前的分辨率是720x1280，绝对坐标转换为相对坐标
        xd_x = (coordinates_x / width) * width
        xd_y = (coordinates_y / height) * height
        driver.tap([(int(xd_x), int(xd_y))])
        # driver.swipe()  # 参数是起/止点坐标

    def task_watched(self, driver, channel):  # 测试激励视频
        driver.find_element_by_android_uiautomator(
            'text("赚豆中心").className("android.widget.TextView").index(1)'
        ).click()
        time.sleep(1)
        try:
            toast_element = WebDriverWait(driver, 5, 1).until(
                lambda x: x.find_element_by_id("tv_watch_immediately")
            )
            toast_element.click()
            time.sleep(45)
            self.relative_coordinates_element(driver, 100, 91)
        except:
            print(f'{channel}渠道包无法观看视频')
        time.sleep(2)
        els1 = driver.find_element_by_id("tv_dialog_reward_cancel")
        els2 = driver.find_element(
            MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("iv_dialog_reward_close")'
        )
        els = random.choice([els1, els2])
        els.click()
        driver.find_element_by_android_uiautomator('resourceId("id_ib_view_actionBar_back")').click()

    def little_game(self, driver, channel, page):  # 测试小游戏
        try:
            time.sleep(2)
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("小游戏").className("android.widget.TextView")'
            ).click()
        except:
            print(f'{channel}无法进入小游戏页面')
        try:
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("欢乐水果切").className("android.widget.TextView")'
            ).click()
            time.sleep(10)
            self.relative_coordinates_element(driver, 526, 1490)
            time.sleep(2)
            self.relative_coordinates_element(driver, 540, 1366)
            time.sleep(60)
            self.relative_coordinates_element(driver, 107, 100)
            driver.press_keycode(AndroidKey.BACK)
            if "欢乐水果切" not in driver.page_source:
                print(f'{channel}渠道包小游戏测试异常)')
            driver.find_element_by_id('leto_iv_back').click()
        except:
            print(f'{channel}渠道包小游戏测试异常')

    def main(self):
        path = r"F:\3.7.7packagerversion"  # 存储APP的路径
        p = 0
        channellist = dict()
        for x in os.listdir(path):
            p += 1
            channel = x.split('_')[1]  # 获取渠道号
            # channel = x.split('.')[0]
            path_pa = path + '\\' + x  # 获取相应包位置的路径
            print(channel)
            pa = self.adbcmdapk(path_pa)
            driver = self.start_appium(pa, path_pa)
            username_and_time = self.one_install_login_sn(driver, channel, p)
            # self.task_watched(driver, channel)
            # self.weChatUserName(driver, channel)
            date_time = self.pay_sn(driver, p, channel)
            # 效验当前账号和渠道包的充值统计点是否正确;
            # db.select_pay_statistics(username_and_time[1], date_time, statistics_id, pa[0], channel)
            print(channel + '渠道包已测试完成' + '——' + str(p))
            bmSpiders = BmSpiders().select_channel_statistics(channel)
            channellist[channel] = bmSpiders
            print(channellist)
            driver.close_app()
            driver.remove_app(pa[0])
            driver.quit()


if __name__ == '__main__':
    Packages().main()