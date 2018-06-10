# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

'''
定义1024网站的数据模型
'''
class XP1024Movie(models.Model):
    pub_id = models.CharField(primary_key=True)  # ID，主见
    pub_name = models.CharField(max_length=255, blank=True, null=True)  # 发布电影的名称
    pub_content =  models.CharField(max_length=1000, blank=True, null=True)  # 发布的内容介绍
    pub_day =  models.CharField(max_length=20, blank=True, null=True)  # 发布日期 年-月-日
    pub_type =  models.CharField(max_length=20, blank=True, null=True)  # 类型，板块类型，亚洲无码
    pub_down_url =  models.CharField(max_length=256, blank=True, null=True)  # 下载的url地址
    pub_img_url =  models.CharField(max_length=128, blank=True, null=True)  # 图片地址
    pub_src =  models.CharField(max_length=20, blank=True, null=True)  # 来源
    pub_info_url =  models.CharField(max_length=128, blank=True, null=True) #影片明细url
    pub_img_size = models.IntegerField(blank=True, null=True)  # 图片的大小

    class Meta:
        managed = False
        db_table = 't_1024xp_movie'



