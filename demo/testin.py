# -*- coding:utf-8 -*-
# @Time    : 2020/10/20 16:10
# @Author  : 年少风狂!
# @File    : testin.py
# @Software: PyCharm

import requests
from openpyxl import Workbook

def devices_info():
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'aliyun_lang=zh; cna=ulsUGNN8uXYCAXH3KRLypCH+; aliyun_site=CN; _HOME_JSESSIONID=02666H71-L35KAL11Z8OUC706MK9X1-8LWVEGGK-O9M9; _home_session0=9pU0k0rgBhpKFAAOYkmD4Vc%2BO0wCWwnBP0Jr9AMsZNMZLTvWHVjp3EzAluEr1uMmjerViHXKk8UUM1vuar96ZOo97kjTG2cP1Y9pBtVNMJe08IBTdpJlgFutBb9FAw6cn0JjHIv5GE1uEu%2BJW%2FLvrjrKqAGhL0uIpNTWjqwhVpdclMj0HHE0SnNhgKFe1V5HRjMzx51AlMftWyDY%2F4g%2BBiWxlNyyQnZ7ZJXYs7IxEqXq7RQquzSQwqVrUwxtXNWgDruNqcMidYQIumigh2AHQ%2BGO%2FNi9wL11kToeqbxsdvYzvuLPxOG%2Fws55VdN1HNJ4xnngxUzdkMQ5Z031W1OCig%3D%3D; consoleNavVersion=1.5.33; console_base_assets_version=3.17.0; XSRF-TOKEN=3d5c16d7-9b6a-4d58-aba1-0075ede816de; _bl_uid=a8kkhgjUgp6eIIwIq80ebIUdR077; t=4eb1104dfe12016455938cf747685f22; _tb_token_=7be6b1e5951ed; cookie2=1fc6da3c6d0623b25106e2ac81fbfa0b; _samesite_flag_=true; xlly_s=1; __yunlog_session__=1603192264865; MQCSESSION=c86ddb61-1dfc-4e33-84a3-839ec586311b; login_aliyunid_csrf=c8a5c35c1b46405dae250420d8163657; login_aliyunid="chenmeiyan @ zhangkong"; login_aliyunid_ticket=wqYo9UWw7R070w3oGFkxbjIFX5nLDTUW2MXONyfhi_ofq1S1E2ml6JYlY4q9CyLstMknfiSc2GhOwNcWzj5bYLpKzKZ49O80KpzxYXWJ0WPzFXDzr7rhZ_Dua5Qyv2KMv85szYAdhP4$; login_aliyunid_sc=74u48x24xL7xCj1SQ9*cYL0T_GM6j755tSkWhoEpZUBKaGKmA*PfwvEnxTC9jSZcOCx2A2hUDMp6mk8EfmshK4j8IyV8JDQ0AckE1AU8iIimoBmc9SaJ3b_ObM2AHYT*; ONE_CONSOLE_NEW_JSESSIONID=f780ecdd-5f49-446c-af29-93b8246deb05; FECS-XSRF-TOKEN=98af037a-6d10-429a-9be0-621d0162155a; FECS-UMID=%7B%22token%22%3A%22Yc1940c5dd8799c210baacdc7efcecc04%22%2C%22timestamp%22%3A%2263765745575F5E46544E6178%22%7D; JSESSIONID=1C26363766DA2B500CCCD19E7B360670; tfstk=cyWNBWXsJReNkmpbwd9q1ZnkHkMOZBsGmv-Wss-0MSDn4EOGiguvxQs6YnT8KCf..; l=eBN2ZhDcOmw1v8CaKO5anurza77tPIRb8sPzaNbMiInca6TC1FGyhNQVtjq6RdtjgtCj7etzaMr08RpAF3f0jNrhUqaBb93n3xJO.; isg=BJCQSvti-5zKyaeaV411t_TsYd7iWXSjrdWY-oph9Ou-xTFvMmlrM46znY0lFSx7',
        'eagleeye-pappname': 'dqu4leglvz@36e3d7771ef0b74',
        'eagleeye-sessionid': 'CdkRwgs8ibwpRemgjjFIkmjaUF3a',
        'eagleeye-traceid': '8ed6273a16031813800201007f0b74',
        'pragma': 'no-cache',
        'referer': 'https://mqciframe.console.aliyun.com/testtools/remotedebug',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    }
    url = 'https://mqciframe.console.aliyun.com/api/device/type/' \
          'get_remote_device_list?filter=all&platformType=ALL&' \
          'projectId=16335&pageSize=-1&pageNum=0' \
          '&filterPublishDate=%5B%5D&_tb_token_=3d5c16d7-9b6a-4d58-aba1-0075ede816de'
    response = requests.get(url, headers=headers)
    print(response.status_code)
    date_json = response.json()
    date = date_json["model"]["items"]
    print(date)
    wb = Workbook()
    ws = wb.create_sheet('阿里云测试机型', index=0)
    ws.append(["品牌", "型号", "系统版本", "操作系统"])
    print(len(date))
    for x in range(540):
        print(x)
        brand = date[x]["brand"]
        model = date[x]["model"]
        platform = date[x]["platform"]
        system = date[x]["system"]
        ws.append([brand, model, platform, system])
    wb.save('阿里云测试机型清单.xlsx')

devices_info()


