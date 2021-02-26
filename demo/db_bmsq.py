# -*- coding:utf-8 -*-
# @Time : 2020/7/17 20:38
# @Author: 年少轻狂
# @File : db_bmsq.py
import pymysql
import requests
import time


class Db(object):

    def __init__(self):
        # 连接不同的数据库
        self.user_db = pymysql.connect(
            'pc-wz9omd329fkh6w63l.rwlb.rds.aliyuncs.com', 'script', 'script1@#$%^', 'bamenuser'
        )
        self.taurus_db = pymysql.connect(
            'bamen-test.rwlb.rds.aliyuncs.com', 'bamen_admin', 'aq1sw2de@#$', 'bamentaurus'
        )
        self.promote_db = pymysql.connect(
            'bamen-test.rwlb.rds.aliyuncs.com', 'bamen_admin', 'aq1sw2de@#$', 'bamenpromote'
        )

    def select_channel_statistics(self, chanel_code):  # 获取不同渠道包对应的统计点
        cur = self.promote_db.cursor()
        sql = f'SELECT channel_no, statistics_id FROM t_promote_box_r_channel WHERE channel_no = "{chanel_code}"'
        cur.execute(sql)
        statistics = cur.fetchone()
        print(f"{chanel_code}渠道对应的统计点是：{statistics[1]}")

        return statistics[1]

    def select_user_id(self, username):  # 查询当前登录账号的用户id
        cur = self.user_db.cursor()
        sql = f'SELECT * FROM t_user_auth_username WHERE username = "{username}" ORDER BY create_time ASC'
        cur.execute(sql)
        user_id = cur.fetchall()

        return user_id

    def select_login_statistics(self, user_id, login_time, chanel_statistics_id, chanel_code):  # 效验登录统计点是否正确
        cur = self.user_db.cursor()
        for x in user_id:  # 根据user_id查询统计点
            try:
                user = x[1]
            except IndexError as e:
                print(f"该用户ID：{x[1]}不是当前账号的用户ID", e)
            else:
                sql = (f'SELECT user_id, statistics_no, android_id, login_time '
                       f'FROM t_user_login_log '
                       f'WHERE user_id = {user} AND login_time > "{login_time}" ORDER BY login_time DESC'
                       )
                cur.execute(sql)
                login_statistics = cur.fetchone()
                if login_statistics:
                    if login_statistics[1] != chanel_statistics_id:
                        print("登录统计点异常！")
                    print(f"{chanel_code}渠道包对应的统计点是：{chanel_statistics_id}; 当前账号实际登录的统计点为{login_statistics[1]}")

    def select_pay_statistics(self, user_ids, pay_time, chanel_statistics_id, package, chanel_code):  # 效验充值统计点是否正确
        cur = self.taurus_db.cursor()
        for index in user_ids:
            user_id = index[1]
            sql = (f'SELECT F_USER_ID, F_TOTAL_AMOUNT, F_STATISTICS_NO, F_VERSION_NAME, F_PACKAGE_NAME, F_CREATE_TIME  '
                   f'FROM t_taurus_bmb_order '
                   f'WHERE F_USER_ID = {user_id} AND F_CREATE_TIME > "{pay_time}" AND F_PAY_STATUS = 0;'
                   )
            cur.execute(sql)
            data = cur.fetchone()
            if data:
                print(data)
                if data[2] != chanel_statistics_id or data[4] != package:
                    print("充值统计点错误!")
                print(f"{chanel_code}渠道包对应的统计点是：{chanel_statistics_id}; 当前账号实际充值的统计点为{data[2]}")


    def close_db(self):
        self.user_db.close()
        self.promote_db.close()
        self.taurus_db.close()


# db = Db()
# statistics_id = db.select_channel_statistics("joke")
# userid = db.select_user_id('ygtester1')
# timedate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# db.select_login_statistics(userid, "2020-07-19 10:19:03", statistics_id, "joke")
# db.select_pay_statistics(userid, "2020-07-19 12:00:11", statistics_id, "com.zhangkongapp.joke.bamenshenqi", 'joke')
# db.close_db()
#




