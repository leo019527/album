#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import MySQLdb
import test

db = MySQLdb.connect("localhost", "root", "123456", "album", charset='utf8' )
cursor = db.cursor()

from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

filename = sys.argv[1]
filepath = sys.argv[2]

'''
appid = 'APPID'
secret_id = 'SECRETID'
secret_key = 'SECRETKEY'
bucket = 'BUCKET'
'''
appid = '1256531249'
secret_id = 'AKIDGK9iwx8IbgYCcoNW1IK8h27wVosg8ZfV'
secret_key = 'iAMIxNxLTKuFJ7fx3uVqwlKdjbEcmhOq'
bucket = 'ocrbucket-1256531249'

client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

'''
#图片鉴黄
#单个或多个图片Url
print (client.porn_detect(CIUrls(['YOUR URL A','YOUR URL B'])))
#单个或多个图片File
print (client.porn_detect(CIFiles(['/Users/lishijie/Desktop/1.jpg',])))
#print (client.porn_detect(CIFiles(['./test.jpg',])))
'''
print '智能鉴黄'
a=client.porn_detect(CIFiles([filepath,]))
print a
if a['result_list'][0]['data']['porn_score']>0.8:
    print 'deleting picture'
    sql = 'delete from picture where picturename="'+filename+'"'
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print '\tdeleting from database success'
        os.remove(filepath)
        print '\tdeleting from fs success'
        # 提交修改xxx
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
        print '\trollback'
    sys.exit(1)

# 图片标签
#单个图片url
#print (client.tag_detect(CIUrl('YOUR URL')))
#单个图片file
print '图片标签'
b = client.tag_detect(CIFile(filepath))
tag = ''
print b['tags']
for c in b['tags']:
    if c['tag_confidence']>50:
        tag += c['tag_name']+','
tag = tag[:-1]
sql = 'update picture set label="'+tag+'" where picturename="'+filename+'"'
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
   print '\tupdate picture.label success'
except:
   # 发生错误时回滚
   db.rollback()
   print '\tupdate picture.label error'

test.Face(filepath)

'''
#OCR-身份证识别
#单个或多个图片Url,识别身份证正面
print (client.idcard_detect(CIUrls(['YOUR URL']), 0))
#单个或多个图片file,识别身份证正面
print (client.idcard_detect(CIFiles(['./id4_zheng.jpg','./id1_zheng.jpg']), 0))
#单个或多个图片Url,识别身份证反面
print (client.idcard_detect(CIUrls(['YOUR URL A', 'YOUR URL B']), 1))
#单个或多个图片file,识别身份证反面
print (client.idcard_detect(CIFiles(['./id5_fan.jpg']), 1))
#单个或多个图片内容,识别身份证反面
if os.path.exists('id5_fan.jpg'):
    print (client.idcard_detect(CIBuffers([open("id5_fan.jpg",'rb').read()]), 1))

#OCR-名片识别    
#单个或多个图片Url
print (client.namecard_detect(CIUrls(['YOUR URL A', 'YOUR URL B']), 0))
#单个或多个图片file
print (client.namecard_detect(CIFiles(['./name1.jpg']), 1))
#单个或多个图片内容,识别名片
if os.path.exists('name1.jpg'):
    print (client.namecard_detect(CIBuffers([open("name1.jpg",'rb').read()]), 1))
	
#人脸检测
#单个图片Url, mode:1为检测最大的人脸 , 0为检测所有人脸
print (client.face_detect(CIUrl('YOUR URL')))
#单个图片file,mode:1为检测最大的人脸 , 0为检测所有人脸
print (client.face_detect(CIFile('./hot2.jpg')))

#五官定位
#单个图片Url,mode:1为检测最大的人脸 , 0为检测所有人脸
print (client.face_shape(CIUrl('YOUR URL'),1))
#单个图片file,mode:1为检测最大的人脸 , 0为检测所有人脸
print (client.face_shape(CIFile('./hot2.jpg'),1))

#创建一个Person, 使用图片url
print (client.face_newperson('person111', ['group2',], CIUrl('YOUR URL'), 'xiaoxin'))
#创建一个Person, 使用图片file
print (client.face_newperson('person211', ['group2',], CIFile('./hot2.jpg')))

#将单个或者多个Face的url加入到一个Person中
print (client.face_addface('person111', CIUrls(['YOUR URL A','YOUR URL B'])))
#将单个或者多个Face的file加入到一个Person中
print (client.face_addface('person211', CIFiles(['./test.jpg',])))

#删除人脸,删除一个person下的face
print (client.face_delface('person111', ['person111',]))

#设置信息
print (client.face_setinfo('person111', 'hello'))

#获取信息
print (client.face_getinfo('person111'))

#获取组列表
print (client.face_getgroupids())

#获取人列表
print (client.face_getpersonids('group2'))

#获取人脸列表
print (client.face_getfaceids('person211'))

#获取人脸信息
print (client.face_getfaceinfo('1820307972625034938'))

#删除个人
print (client.face_delperson('person11'))

#人脸验证,单个图片Url
print (client.face_verify('person111', CIUrl('YOUR URL')))
#人脸验证,单个图片file
print (client.face_verify('person111', CIFile('./test.jpg')))

#人脸检索,单个文件url
print (client.face_identify('group1', CIUrl('YOUR URL')))
##人脸检索,单个文件file
print (client.face_identify('group2', CIFile('./test.jpg')))

#人脸对比
#两个对比图片的文件url
print (client.face_compare(CIFile('./zhao1.jpg'), CIFile('./zhao2.jpg')))
#两个对比图片的文件file
print (client.face_compare(CIUrl('YOUR URL A'), CIUrl('YOUR URL B')))
#一个是图片的文件url， 一个是对比图片的文件file
print (client.face_compare(CIFile('./zhao1.jpg'), CIUrl('YOUR URL C')))

#身份证识别对比
#身份证url
print (client.face_idcardcompare('ID CARD NUM', 'NAME', CIUrl('YOUR URL')))
#身份证文件file
print (client.face_idcardcompare('ID CARD NUM', 'NAME', CIFile('./id4_zheng.jpg')))

#人脸核身
#活体检测第一步：获取唇语（验证码）
obj = client.face_livegetfour()
print (obj)
#验证码
validate_data =''
if 'date' in obj:
    if 'validate_data' in obj['data']:
        validate_data = obj['data']['validate_data']

print (validate_data)
#活体检测第二步：检测
print (client.face_livedetectfour(validate_data, CIFile('../dn.qlv'), False, CIFile('../wxb.jpg')))
#活体检测第二步：检测--对比指定身份信息
print (client.face_idcardlivedetectfour(validate_data, CIFile('../dnn.qlv'), '330782198802084329', '李时杰'))
'''
