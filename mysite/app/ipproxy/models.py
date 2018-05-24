import datetime

from django.db import models


# Create your models here.
class TIpProxy(models.Model):
    host = models.CharField(primary_key=True, max_length=25) #ip:prot 包括ip和端口
    protocol = models.CharField(max_length=20, blank=True, null=True)
    proxy_type = models.IntegerField(blank=True, null=True)
    loc = models.CharField(max_length=20, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    check_time = models.IntegerField(blank=True, null=True)
    src_url = models.CharField(db_column='src_url', max_length=200, blank=True, null=True)

    # 非数据库字段定义
    errorCount = 0 #错误次数,累计错误3次，则把IP放入数据库中
    last_use_time = 0  # 最后使用时间，一般同一个ip在一分钟内不重复使用

    class Meta:
        managed = False
        db_table = 't_ip_proxy'
