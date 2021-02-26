# -*- coding:gbk -*-
# @Time : 2020/7/20 17:29
# @Author: �������
# @File : bmsq_MOD.py
import os
import time
import csv
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait


class Mod(object):
    def __init__(self):
        desired_caps = dict()
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = "10"
        desired_caps["deviceName"] = "xiaomi mix 2s"
        desired_caps["automationName"] = "UiAutomator2"
        desired_caps["appPackage"] = "com.zhangkongapp.joke.bamenshenqi"
        desired_caps["activity"] = "com.joke.bamenshenqi.mvp.ui.activity.LoadingActivity"
        desired_caps["app"] = r'F:\3.7.7packagerversion\bamen.apk'
        desired_caps["unid"] = "2550cbd9"
        desired_caps["unicodeKeyboard"] = False
        desired_caps["resetKeyboard"] = False
        desired_caps["noReset"] = True
        desired_caps["noSign"] = True
        desired_caps["newCommandTimeout"] = 60000
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def enter_mod(self):  # ����MOD������
        time.sleep(4)
        time.sleep(2)
        if "ͬ�Ⲣ����" in self.driver:  # �жϵ�ǰ�豸�Ƿ��״ΰ�װ��app
            wait = WebDriverWait(driver, 3, 1).until(lambda x: x.find_element_by_id('tv_confirm'))
            wait.click()
            time.sleep(1)
            if "ʼ������" in driver.page_source:
                els1 = WebDriverWait(driver, 5, 1).until(
                    lambda x: x.find_element_by_android_uiautomator('text("ʼ������").className("android.widget.Button")')
                )
                els1.click()
                driver.find_element(
                    MobileBy.ANDROID_UIAUTOMATOR, 'text("ʼ������").className("android.widget.Button")'
                ).click()
            else:
                permission = WebDriverWait(driver, 10, 1).until(
                    lambda x: x.find_element_by_id('permission_allow_button'))
                permission.click()
            wait_element = WebDriverWait(driver, 10, 1).until(
                lambda x: x.find_element_by_id('radio_home')
            )
            wait_element.click()
            driver.find_element_by_android_uiautomator('resourceIdMatches(".*radio_home")').click()
            driver.find_element(MobileBy.ANDROID_UIAUTOMATOR,
                                'resourceIdMatches(".*radio_my")'
                                ).click()
        element = WebDriverWait(self.driver, 3, 1).until(
            lambda x: x.find_element_by_id('tag_modifier')
        )
        element.click()

    def game_package(self, filepath):  # ��ȡҪ��װ��������Ϸ�İ�����������
        # if not os.path.exists(filepath):  # �ж�·���Ƿ����
        #     return 0
        # getPackageActivity = 'aapt dump badging %s |findstr "package "' % (filepath) # cmd����̨�Ϲ��˰���������
        # result = os.popen(getPackageActivity).readlines()  # ��ȡcmd����̨����Ϣ�����ȡ������Ϣ
        # print(result)
        # nameNumber = result.find("e='")
        # versionCodeNumber = result.find("' v")
        # package = result[nameNumber + 3:versionCodeNumber]  # ��ȡ������Ϣ�еİ���
        # print(package)
        # return package

        if not os.path.exists(filepath):  # �ж�·���Ƿ����
            return 0
        # cmd����̨�Ϲ��˰���������
        print(23)
        package_activity = 'aapt dump badging %s |findstr "package launchable-activity"' % filepath
        print(package_activity)
        result = os.popen(package_activity).readlines()  # ��ȡcmd����̨����Ϣ�����ȡ������Ϣ
        package_and_activity = list()
        print(result)
        for i in range(len(result)):
            if "package" in result[i]:
                name_number = result[i].find("e='")
                version_code_number = result[i].find("' v")
                package = result[i][name_number + 3:version_code_number]  # ��ȡ����
                package_and_activity.append(package)
            if "launchable-activity" in result[i]:
                name_number = result[i].find("e='")
                version_code_number = result[i].find("'  l")
                activity = result[i][name_number + 3:version_code_number]  # ��ȡ������
                package_and_activity.append(activity)

        return package_and_activity

    def start_mod(self, game_name):
        time.sleep(2)
        self.driver.find_element(
            MobileBy.ANDROID_UIAUTOMATOR, 'resourceIdMatches(".*gotoPhoneapp")'
        ).click()
        time.sleep(2)
        self.driver.find_element_by_id(
            "com.zhangkongapp.joke.bamenshenqi:id/apps_search_edit"
        ).send_keys(game_name)
        try:  # �ж���Ϸ��װ�������Ƿ�ɹ�
            application = self.driver.find_element_by_android_uiautomator(
                f'new UiSelector().text("{game_name}").className("android.widget.TextView")'
            )
            if application.text == game_name:
                TouchAction(self.driver).tap(x=920, y=500).perform()
                time.sleep(5)
        except:
            print(f'{game_name}��Ϸ����δ��װ�ɹ�')
        try:
            TouchAction(self.driver).tap(x=920, y=500).perform()
            self.driver.find_element(
                MobileBy.ANDROID_UIAUTOMATOR, 'text("MOD����").className("android.widget.Button")'
            ).click()
        except:
            print(f'{game_name}��ϷMOD����δ�ɹ�')
        if "ȥ����" in self.driver.page_source and "������Ȩ��" in self.driver.page_source:
            wait_element = WebDriverWait(self.driver, 3, 1).until(
                lambda x: x.find_element_by_id("pl_check_bind_tel_bt")
            )
            wait_element.click()
            # self.driver.find_element_by_android_uiautomator(
            #     'new UiSelector().resourceId("com.zhangkongapp.joke.bamenshenqi:id/pl_check_bind_tel_bt")'
            # ).click()

            element = WebDriverWait(self.driver, 3, 1).until(
                lambda x: x.find_element_by_id("title")
            )
            element.click()
            up_element = WebDriverWait(self.driver, 3, 1).until(
                lambda x: x.find_element_by_accessibility_id("����")
            )
            up_element.click()
            self.driver.find_element_by_android_uiautomator(
               'text("MOD����").className("android.widget.Button")'
            ).click()
        time.sleep(7)
        # self.driver.start_activity(package_and_activity[0], package_and_activity[1])
        if "Google Play ����" in self.driver.page_source and f"{game_name}" in self.driver.page_source:
            self.driver.find_element_by_id("android:id/button1").click()
        TouchAction(self.driver).tap(x=62, y=576).perform()
        TouchAction(self.driver).tap(x=45, y=1077).perform()
        if "����¼��" in self.driver.page_source and "�����Ƽ�" in self.driver.page_source:
            print(f'{game_name}��Ϸ����ͨ��')

    def main(self):
        self.enter_mod()
        path = r"F:\mod_game"  # �洢APP��·��
        # path = r"F:\python_bmsq_code\mod_game"
        for index in os.listdir(path):
            game_name = index.split(".apk")[0]  # ��ȡ��Ϸ��
            print(game_name)
            game_path = path + "\\" + index  # ��ȡ��Ϸλ�õľ���·��
            print(game_path)
            # package_and_activity = self.game_package(game_path)
            # print(package_and_activity)
            # os.system("adb install" + index)
            os.popen(f'adb install {game_path}')
            self.driver.install_app(game_path, timeout=600000)
            print(f"{game_name}��װ�ɹ�")
            self.start_mod(game_name)
            # self.driver.remove_app(package_and_activity[0])


if __name__ == '__main__':
    Mod().main()

