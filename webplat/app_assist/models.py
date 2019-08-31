from django.db import models
from mongoengine import *

# Create your models here

# 指明要连接的数据库
#connect ('mydb',host = '127.0.0.1', port = 27017)

class inviatation(Document):
    #定义数据库中的所有字段
    gnb = StringField()   #ip-user-password
    end = StringField()   #ip-user-password
    ue  = StringField()   #ip
    nagvm_ip = StringField() #ip
    nr_tue = StringField() #ip
    lte_tue = StringField() #ipmeta = {'collection':'invitation'}
    aau = StringField() #detail
    owner = StringField()
    count = IntField()
    # 指明连接的数据表明
    meta = {'collection':'invitation'}

#测试是否连接成功
#for i in invitation.objects[:10]:
#   print(i.title)
class history(Document):
    # 定义数据库中的所有字段
    CSI_RSRP = StringField()
    CIS_SINR = StringField()
    MCS = StringField()
    RB = StringField()
    iBLER = StringField()
    MAC_Thp = StringField()
    Rank = StringField()
    # 指明连接的数据库表明
    meta = {'collection':'history'}

class testresult(Document):
    # 定义数据库中的所有字段
    operator = StringField()
    test_date = StringField()
    case_name = StringField()
    test_edition = StringField()
    net_type = StringField()
    ant_type = StringField()
    frequency_band = StringField()
    bandwidth = StringField()
    ul_or_dl = StringField()
    subframe_ratio = StringField()
    additional_description = StringField()
    # data_path = StringField()
    # result_path = StringField()
    # result = StringField()
    # 指明连接的数据表名
    meta = {'collection':'testresult'}