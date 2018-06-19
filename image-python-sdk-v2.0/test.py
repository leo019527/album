#!/usr/bin/env python
# -*- coding: utf-8 -*-
##从qcloud_image包导入相关
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers
import requests, urllib3, pymssql


def Face(filename):
    appid = '1256531249'
    secret_id = 'AKIDGK9iwx8IbgYCcoNW1IK8h27wVosg8ZfV'
    secret_key = 'iAMIxNxLTKuFJ7fx3uVqwlKdjbEcmhOq'
    bucket = 'ocrbucket-1256531249'
    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)

    if client.face_detect(CIFile('test2.jpeg'), 1).get('message') == 'OK': #如果监测到人脸进行如下操作
        # 数据库连接
        conn = pymssql.connect('localhost', 'root', '123456', 'album')
        cursor = conn.cursor()

        # 数据库查询操作
        cursor.execute('SELECT name FROM names')
        row = cursor.fetchone()
        flag = 0

        id = 1
        # 对于每一个查询到的人名
        while row:
            id = id + 1
            # print("ID=%d, Name=%s" % (row[0], row[1]))
            if client.face_verify(row, CIFile(filename)).get('data').get('confidence') > 90:  # 若跟这个人置信度大于90
                print(client.face_addface(row, CIFiles([filename, ])))  # 就加脸
                flag = 1
                break
            else:
                # 取下个人名继续判断
                row = cursor.fetchone()

        # 若判断完仍未找到对的人
        if flag == 0:
            client.face_newperson('人物' + str(id), ['group1', ], CIFile(filename))  # 就添加新人
            # 并将其插入到数据库中
            cursor.executemany(
                "INSERT INTO names VALUES (%s)", [('人物' + str(id))])
            # 如果没有指定autocommit属性为True的话就需要调用commit()方法
            conn.commit()

            cursor.executemany(
                "UPDATE picture SET namelabel ='"+'人物' + str(id)+"' where pictureid='"+filename+"'")