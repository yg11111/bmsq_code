# -*- coding:utf-8 -*-
# @Time : 2020/7/13 12:50
# @Author: 年少轻狂(yg)
# @File : bmsq_packages.py

import sys
import os
import time
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bm_channel_packages.equipment_information import Equipment
from bm_channel_packages.bm_background import BmSpiders
from bm_channel_packages.taurus_selenium import LoginSpider


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
        desired_caps["appActivity"] = package_and_activity[1]
        desired_caps["app"] = app_path
        desired_caps["unid"] = Equipment().unid()
        desired_caps["unicodeKeyboard"] = False
        desired_caps["resetKeyboard"] = False
        desired_caps["noReset"] = True
        desired_caps["noSign"] = True
        desired_caps["newCommandTimeout"] = 60000
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        return driver

    def login_sn(self, driver):
        time.sleep(2.0)
        if "同意并继续" in driver.page_source:  # 判断当前设备是否首次安装该app
            wait = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id('tv_right'))
            wait.click()
            time.sleep(1)
            if "始终允许" in driver.page_source:
                els1 = WebDriverWait(driver, 5, 1).until(
                    lambda x: x.find_element_by_android_uiautomator('text("始终允许").className("android.widget.Button")')
                )
                els1.click()
                driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("始终允许").className("android.widget.Button")'
                ).click()
            else:
                permission = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_id('permission_allow_button'))
                permission.click()
        els2 = WebDriverWait(driver, 20, 1).until(lambda x: x.find_element_by_id('tag_3'))
        els2.click()
        driver.find_element(
            MobileBy.ANDROID_UIAUTOMATOR, 'text("我的").className("android.widget.RadioButton")'
        ).click()
        username = driver.find_element(MobileBy.ID, "tv_user_name").text

        return username

    def one_install_login_sn(self, driver, channel, p, channel_statistics):  # 判断用户是否首次安装该app以及登录状态、登录统计点上报
        if "立即登录" in driver.page_source:  # 判断当前账号是否已登录
            driver.find_element(MobileBy.ID, "iv_head_icon").click()
            self.third_party_login(driver, channel)
            time.sleep(1)
            username = driver.find_element(MobileBy.ID, "id_tv_view_userInfo_username").text
            els = WebDriverWait(driver, 5, 1).until(
                lambda x: x.find_element_by_android_uiautomator('resourceIdMatches(".*id_ib_view_actionBar_back")')
            )
            els.click()
        else:
            element = WebDriverWait(driver, 20, 1).until(lambda x: x.find_element_by_id("iv_setting"))
            element.click()
            time.sleep(2)
            els2 = WebDriverWait(driver, 20, 1).until(
                lambda x: x.find_element_by_android_uiautomator('text("切换账号").className("android.widget.TextView")')
            )
            els2.click()
            self.third_party_login(driver, channel)
            time.sleep(2)
            username = driver.find_element(MobileBy.ID, "id_tv_view_userInfo_username").text
            els3 = WebDriverWait(driver, 10, 1).until(
                lambda x: x.find_element_by_android_uiautomator('resourceIdMatches(".*id_ib_view_actionBar_back")')
            )
            els3.click()
        time_and_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        loginstatistics_and_time = BmSpiders().select_login_statistics(username)
        compare_time = int(time.mktime(time.strptime(time_and_date, "%Y-%m-%d %H:%M:%S"))) \
                    - int(time.mktime(time.strptime(loginstatistics_and_time[1], "%Y-%m-%d %H:%M:%S")))
        if (loginstatistics_and_time[0] != channel_statistics) and (compare_time <= 30):
            print(f'{channel}渠道包登录统计点错误')
            print(f'{channel}渠道包的统计点是{channel_statistics},当前登录获取的统计点是{loginstatistics_and_time[0]}')

        return username

    def third_party_login(self, driver, channel):  # 测试第三方登录
        time.sleep(3)
        if "本机号码一键登录" in driver.page_source:
            try:
                driver.find_element_by_id('qq').click()
                time.sleep(5)
                if "设置账密" in driver.page_source:  # 判断当前账号登录QQ是否首次登录
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                elif "QQ授权登录" in driver.page_source:
                    element = WebDriverWait(driver, 10, 1).until(
                        lambda x: x.find_element_by_id("com.tencent.mobileqq:id/fds")
                    )
                    element.click()
                else:
                    pass
                toast_element = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                time.sleep(1)
                toast = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if ("登录成功" not in toast.text) or ("授权成功" not in toast_element.text):
                    print(toast_element.text, toast.text)
            except:
                print(f'{channel}渠道包qq登录异常')
            time.sleep(1)
            els = WebDriverWait(driver, 5, 1).until(lambda x: x.find_element_by_android_uiautomator(
                'text("切换账号").className("android.widget.TextView")'
            ))
            els.click()
            try:
                time.sleep(1)
                driver.find_element_by_id('weibo').click()
                time.sleep(3)
                if "设置账密" in driver.page_source:
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                toast_element = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                time.sleep(1)
                toast = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if ("登录成功" not in toast.text) or ("授权成功" not in toast_element.text):
                    print(toast_element.text, toast.text)
            except:
                print(f'{channel}渠道包微博登录异常')
            time.sleep(1)
            driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("切换账号").className("android.widget.TextView")'
            ).click()
            try:
                time.sleep(2)
                driver.find_element_by_id('weixin').click()
                if "设置账密" in driver.page_source:
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                time.sleep(3)
                toast_element = WebDriverWait(driver, 20, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                time.sleep(1)
                toast = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if ("登录成功" not in toast.text) or ("授权成功" not in toast_element.text):
                    print(toast_element.text, toast.text)
            except:
                print(f'{channel}渠道包微信登录异常')
        else:
            try:
                driver.find_element_by_id('qq_login').click()
                time.sleep(2)
                if "设置账密" in driver.page_source:  # 判断当前账号登录QQ是否首次登录
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()
                elif "QQ授权登录" in driver.page_source:
                    element = WebDriverWait(driver, 10, 1).until(
                        lambda x: x.find_element_by_id("com.tencent.mobileqq:id/fds")
                    )
                    element.click()
                else:
                    pass
                toast_element = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                time.sleep(1)
                toast = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if ("登录成功" not in toast.text) or ("授权成功" not in toast_element.text):
                    print(toast_element.text, toast.text)
            except:
                print(f'{channel}渠道包qq登录异常')
            time.sleep(1)
            els = WebDriverWait(driver, 10, 1).until(lambda x: x.find_element_by_android_uiautomator(
                'text("切换账号").className("android.widget.TextView")'
            ))
            els.click()
            # try:
            #     time.sleep(1)
            #     driver.find_element_by_id('sina_login').click()
            #     time.sleep(3)
            #     if "设置账密" in driver.page_source:
            #         driver.find_element(MobileBy.ID, 'tv_right').click()
            #         driver.find_element(
            #             MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
            #         ).click()
            #     toast_element = WebDriverWait(driver, 20, 1).until(
            #         lambda x: x.find_element_by_xpath("//android.widget.Toast")
            #     )
            #     time.sleep(1)
            #     toast = WebDriverWait(driver, 10, 1).until(
            #         lambda x: x.find_element_by_xpath("//android.widget.Toast")
            #     )
            #     if ("登录成功" not in toast.text) or ("授权成功" not in toast_element.text):
            #         print(toast_element.text, toast.text)
            # except:
            #     print(f'{channel}渠道包微博登录异常')
            # time.sleep(1)
            # driver.find_element(
            #     MobileBy.ANDROID_UIAUTOMATOR, 'text("切换账号").className("android.widget.TextView")'
            # ).click()
            try:
                time.sleep(1)
                driver.find_element_by_id('weixin_login').click()
                if "设置账密" in driver.page_source:
                    driver.find_element(MobileBy.ID, 'tv_right').click()
                    driver.find_element(
                        MobileBy.ANDROID_UIAUTOMATOR, 'className("android.widget.ImageButton")'
                    ).click()

                toast_element = WebDriverWait(driver, 3, 1).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Toast")
                )
                if ("授权成功" not in toast_element.text):
                    print(toast_element.text)
            except:
                print(f'{channel}渠道包微信登录异常')

    def pay_sn(self, driver, p, channel):  # 充值统计点上报
        driver.find_element(
            MobileBy.ID, "tv_bm_currency"
        ).click()
        wait = WebDriverWait(driver, 3, 1).until(
            lambda x: x.find_element_by_xpath('//android.widget.LinearLayout/android.widget.Button')
            )
        wait.click()
        if "下次再说" in driver.page_source:  # 判断当前账号是否绑定手机号
            els4 = WebDriverWait(driver, 20, 1).until(lambda x: x.find_element_by_id('tv_left'))
            els4.click()
        data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 拉起微信支付
        time.sleep(1)
        if p % 2 != 0:
            try:
                wx_pay = driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("微信支付").className("android.widget.TextView")'
                )
                wx_pay.click()
                els = WebDriverWait(driver, 25, 1).until(lambda x: x.find_element_by_id(
                                                        'com.tencent.mm:id/eh')
                                                        )
                els.click()
                element = WebDriverWait(driver, 20, 1).until(
                    lambda x: x.find_element_by_android_uiautomator(
                        'resourceId("com.tencent.mm:id/ffp")'
                    ))
                element.click()
            except:
                print(channel + "渠道包，充值异常")
        # 拉起支付宝支付
        else:
            try:
                zfb_pay = driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("支付宝").className("android.widget.TextView")'
                )
                zfb_pay.click()
                # driver.start_activity("com.eg.android.AlipayGphone",
                #                       "com.alipay.android.msp.ui.views.MspContainerActivity"
                #                       )
                wait = WebDriverWait(driver, 25, 1).until(lambda x: x.find_element_by_accessibility_id("退出"))
                wait.click()
                els1 = WebDriverWait(driver, 20, 1).until(lambda x: x.find_element_by_id(
                    "com.alipay.mobile.antui:id/cancel"
                ))
                els1.click()
            except:
                print(print(channel + "渠道包，充值异常"))

        if p % 2 == 0:
            element_wait = WebDriverWait(driver, 20, 1).until(
                lambda x: x.find_element_by_android_uiautomator(
                    'text("我没有支付").className("android.widget.Button").index(0)'
                ))
            # prompt_cancel = driver.find_element_by_xpath('//android.widget.LinearLayout/android.widget.Button[1]')
            element_wait.click()
            try:
                toast_loc = ("xpath", ".//android.widget.Toast")
                toast_element = WebDriverWait(driver, 5, 1).until(ec.presence_of_element_located(toast_loc))
                if '支付失败' not in toast_element.text:
                    print(toast_element.text)
            except:
                print(channel + "渠道包，充值toast异常")

        else:
            prompt_ok_bt = WebDriverWait(driver, 20, 1).until(lambda x: x.find_element_by_android_uiautomator(
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

    def main(self):
        path = r"E:\hgyx-packages"  # 存储APP的路径
        p = 0
        channellist = list()
        BmSpiders().get_token()
        LoginSpider().login()
        for x in os.listdir(path):
            if x.split('_')[1] in channellist:
                continue
            p += 1
            channel = x.split('_')[1]  # 获取渠道号
            path_pa = path + '\\' + x  # 获取相应包位置的路径
            pa = self.adbcmdapk(path_pa)
            channel_statistics = BmSpiders().select_channel_statistics(channel)
            driver = self.start_appium(pa, path_pa)
            self.login_sn(driver)
            username = self.one_install_login_sn(driver, channel, p, channel_statistics)
            self.pay_sn(driver, p, channel)
            package_statisticsNo = LoginSpider().main(username)
            if (package_statisticsNo[0] != pa[0]) or (package_statisticsNo[1] != channel_statistics):
                print(f'{channel}渠道包充值统计点错误')
                print(f'{channel}渠道包的统计点是{channel_statistics},当前充值获取的统计点是{package_statisticsNo[1]}')
            print(channel + '渠道包已测试完成' + '——' + str(p))
            channellist.append(channel)
            driver.close_app()
            driver.remove_app(pa[0])
            driver.quit()


if __name__ == '__main__':
    Packages().main()
