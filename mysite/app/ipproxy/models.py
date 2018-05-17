import datetime

from django.db import models

# Create your models here.
class TIpProxy(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    prot = models.IntegerField(blank=True, null=True)
    protocol = models.CharField(max_length=20, blank=True, null=True)
    proxy_type = models.IntegerField(blank=True, null=True)
    loc = models.CharField(max_length=20, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    check_time = models.IntegerField(blank=True, null=True)
    src_url = models.CharField(db_column='src_url',max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_ip_proxy'


