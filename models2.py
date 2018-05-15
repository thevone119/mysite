# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class TIpProxy(models.Model):
    ip = models.CharField(primary_key=True, max_length=20)
    prot = models.IntegerField(blank=True, null=True)
    protocol = models.CharField(max_length=20, blank=True, null=True)
    proxy_type = models.IntegerField(blank=True, null=True)
    loc = models.CharField(max_length=20, blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    check_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_ip_proxy'


class TMapCfgArea(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128, blank=True, null=True)
    blng = models.CharField(max_length=20, blank=True, null=True)
    blat = models.CharField(max_length=20, blank=True, null=True)
    glng = models.CharField(max_length=20, blank=True, null=True)
    glat = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(db_column='create_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    layer_id = models.CharField(db_column='LAYER_id', max_length=20, blank=True, null=True)  # Field name made lowercase.
    area_type = models.CharField(max_length=20, blank=True, null=True)
    area_radius = models.CharField(max_length=20, blank=True, null=True)
    area_aspect = models.CharField(max_length=20, blank=True, null=True)
    area_border_gps = models.TextField(blank=True, null=True)
    area_border_baidu = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_map_cfg_area'


class TMapCfgAreaPoint(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128, blank=True, null=True)
    blng = models.CharField(max_length=20, blank=True, null=True)
    blat = models.CharField(max_length=20, blank=True, null=True)
    glng = models.CharField(max_length=20, blank=True, null=True)
    glat = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(db_column='create_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    layer_id = models.CharField(db_column='LAYER_id', max_length=20, blank=True, null=True)  # Field name made lowercase.
    area_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_map_cfg_area_point'


class TMapCfgLayer(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128, blank=True, null=True)
    blng = models.CharField(max_length=20, blank=True, null=True)
    blat = models.CharField(max_length=20, blank=True, null=True)
    glng = models.CharField(max_length=20, blank=True, null=True)
    glat = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(db_column='create_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_map_cfg_layer'


class TMapPointChange(models.Model):
    blat = models.FloatField(blank=True, null=True)
    blng = models.FloatField(blank=True, null=True)
    glat = models.FloatField(blank=True, null=True)
    glng = models.FloatField(blank=True, null=True)
    createtime = models.CharField(max_length=20, blank=True, null=True)
    batch = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_map_point_change'


class TMvMovie(models.Model):
    smd532 = models.CharField(max_length=32, blank=True, null=True)
    smd5 = models.CharField(max_length=32, blank=True, null=True)
    slen = models.BigIntegerField(blank=True, null=True)
    sname = models.CharField(max_length=255, blank=True, null=True)
    fullfilename = models.CharField(db_column='FullFileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sctime = models.BigIntegerField(db_column='Sctime', blank=True, null=True)  # Field name made lowercase.
    createtime = models.BigIntegerField(db_column='CreateTime', blank=True, null=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version', blank=True, null=True)  # Field name made lowercase.
    hreadlen = models.IntegerField(db_column='Hreadlen', blank=True, null=True)  # Field name made lowercase.
    iszip = models.SmallIntegerField(db_column='IsZip', blank=True, null=True)  # Field name made lowercase.
    byteadd = models.SmallIntegerField(db_column='Byteadd', blank=True, null=True)  # Field name made lowercase.
    zipstate = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_mv_movie'


class TSysDbGenerator(models.Model):
    sequence_name = models.CharField(db_column='SEQUENCE_NAME', primary_key=True, max_length=128)  # Field name made lowercase.
    sequence_next_hi_value = models.IntegerField(db_column='SEQUENCE_NEXT_HI_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_sys_db_generator'


class TTbCategory(models.Model):
    cid = models.IntegerField(db_column='CID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=128, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    pcid = models.IntegerField(db_column='PCID', blank=True, null=True)  # Field name made lowercase.
    create_time = models.CharField(db_column='create_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_tb_category'


class TTbShop(models.Model):
    shopid = models.BigIntegerField(db_column='shopId', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=128, blank=True, null=True)
    sdesc = models.CharField(max_length=128, blank=True, null=True)
    bulletin = models.CharField(max_length=128, blank=True, null=True)
    mainpage = models.CharField(max_length=128, blank=True, null=True)
    nick = models.CharField(max_length=128, blank=True, null=True)
    main_cid = models.IntegerField(blank=True, null=True)
    main_cname = models.CharField(max_length=128, blank=True, null=True)
    seller_credit = models.IntegerField(blank=True, null=True)
    shop_createtime = models.CharField(max_length=20, blank=True, null=True)
    shop_area = models.CharField(max_length=20, blank=True, null=True)
    shop_score = models.FloatField(blank=True, null=True)
    item_score = models.FloatField(blank=True, null=True)
    service_score = models.FloatField(blank=True, null=True)
    delivery_score = models.FloatField(blank=True, null=True)
    shop_type = models.CharField(max_length=10, blank=True, null=True)
    create_time = models.CharField(db_column='create_Time', max_length=14, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=14, blank=True, null=True)  # Field name made lowercase.
    goodrate_percent = models.FloatField(blank=True, null=True)
    sales_count = models.IntegerField(blank=True, null=True)
    prod_count = models.IntegerField(blank=True, null=True)
    user_rate_url = models.CharField(db_column='user_Rate_Url', max_length=128, blank=True, null=True)  # Field name made lowercase.
    uid = models.BigIntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    prod_loc = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tb_shop'


class TTbShopData(models.Model):
    keyid = models.AutoField(primary_key=True)
    shopid = models.IntegerField(db_column='shopId')  # Field name made lowercase.
    sales_count = models.IntegerField(blank=True, null=True)
    store_count = models.IntegerField(blank=True, null=True)
    sales_money = models.IntegerField(blank=True, null=True)
    max_prod_sales = models.IntegerField(blank=True, null=True)
    max_pord_store = models.IntegerField(blank=True, null=True)
    count_time = models.IntegerField(db_column='count_Time', blank=True, null=True)  # Field name made lowercase.
    seller_credit = models.IntegerField(blank=True, null=True)
    shop_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tb_shop_data'


class TTbShopProd(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    shopid = models.BigIntegerField(blank=True, null=True)
    outer_id = models.CharField(max_length=128, blank=True, null=True)
    cid = models.IntegerField(blank=True, null=True)
    cat_name = models.CharField(max_length=128, blank=True, null=True)
    commodity_id = models.IntegerField(blank=True, null=True)
    created = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    prod_desc = models.CharField(max_length=256, blank=True, null=True)
    modified = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    sale_num = models.IntegerField(blank=True, null=True)
    rate_num = models.IntegerField(blank=True, null=True)
    shop_price = models.IntegerField(blank=True, null=True)
    standard_price = models.IntegerField(blank=True, null=True)
    vertical_market = models.IntegerField(blank=True, null=True)
    update_time = models.CharField(db_column='update_Time', max_length=14, blank=True, null=True)  # Field name made lowercase.
    create_time = models.CharField(db_column='create_Time', max_length=14, blank=True, null=True)  # Field name made lowercase.
    uid = models.BigIntegerField(db_column='UID', blank=True, null=True)  # Field name made lowercase.
    loc = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tb_shop_prod'


class TTbShopProdData(models.Model):
    keyid = models.AutoField(db_column='KEYID', primary_key=True)  # Field name made lowercase.
    product_id = models.IntegerField(blank=True, null=True)
    shopid = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    sale_num = models.IntegerField(blank=True, null=True)
    rate_num = models.IntegerField(blank=True, null=True)
    shop_price = models.IntegerField(blank=True, null=True)
    standard_price = models.IntegerField(blank=True, null=True)
    count_time = models.IntegerField(db_column='count_Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_tb_shop_prod_data'


class TTbUser(models.Model):
    uid = models.BigIntegerField(db_column='uId', primary_key=True)  # Field name made lowercase.
    nick = models.CharField(max_length=128, blank=True, null=True)
    sex = models.CharField(max_length=4, blank=True, null=True)
    userpage = models.CharField(max_length=128, blank=True, null=True)
    seller_credit = models.IntegerField(blank=True, null=True)
    buy_credit = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(db_column='create_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_time = models.CharField(db_column='update_Time', max_length=20, blank=True, null=True)  # Field name made lowercase.
    register_time = models.CharField(max_length=20, blank=True, null=True)
    user_account = models.CharField(max_length=32, blank=True, null=True)
    loc = models.CharField(max_length=20, blank=True, null=True)
    main_cid = models.IntegerField(blank=True, null=True)
    main_cname = models.CharField(max_length=32, blank=True, null=True)
    user_rate_url = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_tb_user'


class TTempObj(models.Model):
    obj_key = models.CharField(primary_key=True, max_length=32)
    obj_value = models.CharField(max_length=1000, blank=True, null=True)
    obj_type = models.CharField(max_length=64, blank=True, null=True)
    create_time = models.BigIntegerField(blank=True, null=True)
    expire_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_temp_obj'
