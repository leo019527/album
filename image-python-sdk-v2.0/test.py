#!/usr/bin/env python
# -*- coding: utf-8 -*-
##从qcloud_image包导入相关
from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers
import requests, urllib3, pymssql
import MySQLdb


def Face(filename):
    appid = '1256531249'
    secret_id = 'AKIDGK9iwx8IbgYCcoNW1IK8h27wVosg8ZfV'
    secret_key = 'iAMIxNxLTKuFJ7fx3uVqwlKdjbEcmhOq'
    bucket = 'ocrbucket-1256531249'
    client = Client(appid, secret_id, secret_key, bucket)
    client.use_http()
    client.set_timeout(30)
    print '人脸识别'

    if client.face_detect(CIFile(filename), 1).get('message') == 'OK': #如果监测到人脸进行如下操作
        print 'indect face'
        # 数据库连接
        #conn = pymssql.connect('localhost', 'root', '123456', 'album')
        db = MySQLdb.connect("localhost", "root", "123456", "album", charset='utf8' )
        cursor = db.cursor()

        # 数据库查询操作
        cursor.execute('SELECT name FROM names')
        row = cursor.fetchone()
        flag = 0

        id = 1
        # 对于每一个查询到的人名
        while row:
            id = id + 1
            # print("ID=%d, Name=%s" % (row[0], row[1]))
            if client.face_verify(row[0], CIFile(filename)).get('data').get('confidence') > 90:  # 若跟这个人置信度大于90
                print '\t\tget '+row[0]
                client.face_addface(row[0], CIFiles([filename, ]))  # 就加脸
                sql = "update picture set namelabel='"+row[0]+"' where pictureid='"+filename.replace('/home/ubuntu/album/public/',"")+"'"
                try:
                    cursor.execute(sql)
                    db.commit()
                    print 'update namelabel success'
                except:
                    db.rollback()
                    print "update namelabel error"
                flag = 1
                break
            else:
                # 取下个人名继续判断
                row = cursor.fetchone()

        # 若判断完仍未找到对的人
        if flag == 0:
            client.face_newperson('people' + str(id), ['group1', ], CIFile(filename))  # 就添加新人
            try:
                # 并将其插入到数据库中
                cursor.execute(
                    "INSERT INTO names VALUES( '"+'people' + str(id)+"')")
                # 如果没有指定autocommit属性为True的话就需要调用commit()方法
                db.commit()
                print 'insert names success'
            except:
                db.rollback()
                print 'insert names error'
            
            try:
                cursor.execute(
                    "UPDATE picture SET namelabel ='"+'people' + str(id)+"' where pictureid='"+filename.replace('/home/ubuntu/album/public/',"")+"'")
                db.commit()
                print 'update picture.namelabel success'
            except:
                db.rollback()
                print 'update picture.namelabel success'
        db.close()
