# -*- coding:utf-8 -*-
# @Time : 2020-07-05 17:41 
# @Author : xx
# @File : mysql_bmsq.py 
# @Software: PyCharm
import requests
import lxml
import selenium
import pymysql

db = pymysql.connect(  # 连接数据库
	'bamen-test.rwlb.rds.aliyuncs.com',
	'bamen_admin',
	'aq1sw2de@#$',
	'bamenuser'
	)
# cur = db.cursor()  # 使用cursor()方法获取操作游标
cur = db.cursor(cursor=pymysql.cursors.DictCursor)  # 创建游标，操作设置为字典类型
cur.execute("select * from t_user_auth_username where username='ygtester1'")
# data = cur.fetchone()  # 获取返回结果下一行的数据
# data = cur.fetchall()  # 获取返回结果所有行的数据，返回元组
data = cur.fetchmany(1)  # 获取返回结果指定行的数据
result = cur.rowcount  # 返回结果数据的行数
print(data)
print(cur.rowcount)
# print(f'ygtester1的用户ID为:{data[1]}')
# print(type(data))
db.close()  # 关闭数据库连接


# try:
#    # 执行SQL语句
#    cursor.execute(sql)
#    # 获取所有记录列表
#    results = cursor.fetchall()
#    for row in results:
#       fname = row[0]
#       lname = row[1]
#       age = row[2]
#       sex = row[3]
#       income = row[4]
#        # 打印结果
#       print ("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
#              (fname, lname, age, sex, income ))
# except:
#    print ("Error: unable to fetch data")
