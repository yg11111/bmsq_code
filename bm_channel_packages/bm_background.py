# -*- coding:utf-8 -*-
# @Time    : 2020/8/17 17:25
# @Author  : 年少风狂!
# @File    : bm-background.py
# @Software: PyCharm
import requests
import json


class BmSpiders(object):
    def __init__(self):
        self.start_url = "http://adminnew.bamenzhushou.com/"

    def get_token(self):  # 获取登录八门后台的token
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.89 Safari/537.36'
        }
        url = f'{self.start_url}v1/admin/user/login/username'
        data = {"username": "yangguang", "password": "yangg079."}
        response = requests.post(url, data=data, headers=headers)
        html = response.text
        usertoken = json.loads(html)
        token = usertoken['content']['userToken']['token']
        with open('token.txt', 'w') as f:
            f.write(token)

    def select_login_statistics(self, username):  # 获取当前账号最后一次登录的统计点
        try:
            with open('token.txt', 'r') as f:
                token = f.read()
            url = f"{self.start_url}api/user-admin/v1/platform-user-login-log/page?"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/84.0.4147.89 Safari/537.36',
                'Authorization': token
            }
            params = {
                "pageNum": 1,
                "pageSize": 10,
                "userName": username
            }
            response = requests.get(url, params=params, headers=headers)
            html = response.text
            statistics = json.loads(html)
            login_time = statistics["content"]["content"][0]["loginTime"]

        except:
            self.get_token()
            with open('token.txt', 'r') as f:
                token = f.read()
            url = f"{self.start_url}api/user-admin/v1/platform-user-login-log/page?"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/84.0.4147.89 Safari/537.36',
                'Authorization': token
            }
            params = {
                "pageNum": 1,
                "pageSize": 10,
                "userName": username
            }
            response = requests.get(url, params=params, headers=headers)
            html = response.text
            statistics = json.loads(html)
            login_time = statistics["content"]["content"][0]["loginTime"]
        
        return statistics["content"]["content"][0]["statisticsNo"], login_time

    def select_channel_statistics(self, channelNo):  # 获取不同渠道包对应的统计点
        try:
            with open('token.txt', 'r') as f:
                token = f.read()
            url = f'{self.start_url}api/promote-new-admin/v1/channel/list?'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/84.0.4147.89 Safari/537.36',
                'Referer': f'{self.start_url}/pages/platform/list_channel.html',
                'Authorization': token
            }
            params = {
                "pageNum": 1,
                "pageSize": 10,
                "channelNo": channelNo
            }
            response = requests.get(url, params=params, headers=headers)
            html = response.text
            channelNo_statistics = json.loads(html)

        except:
            self.get_token()
            with open('token.txt', 'r') as f:
                token = f.read()
            url = f'{self.start_url}api/promote-new-admin/v1/channel/list?'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/84.0.4147.89 Safari/537.36',
                'Referer': f'{self.start_url}/pages/platform/list_channel.html',
                'Authorization': token
            }
            params = {
                "pageNum": 1,
                "pageSize": 10,
                "channelNo": channelNo
            }
            response = requests.get(url, params=params, headers=headers)
            html = response.text
            channelNo_statistics = json.loads(html)

        return channelNo_statistics["content"][0]["statisticsId"]
