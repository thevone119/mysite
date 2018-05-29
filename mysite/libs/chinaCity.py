# -*- coding: utf-8 -*-
# 中国的省份，城市列表
import threading

# 省会城市
PROV_CITY = ['太原', '长春', '南京', '合肥', '南昌', '郑州', '长沙', '海口', '贵阳', '西安', '西宁', '呼和浩特', '拉萨', '乌鲁木齐', '石家庄', '沈阳', '哈尔滨',
             '杭州', '福州', '济南', '广州', '武汉', '成都', '昆明', '兰州', '台北', '南宁', '银川']

# 广东城市
GD_CITY = ['广州', '深圳', '东莞', '中山', '珠海', '汕头', '佛山', '韶关', '湛江', '肇庆', '江门', '茂名', '惠州', '梅州', '汕尾', '河源', '阳江', '清远',
           '潮州', '揭阳', '云浮']

# 省、直辖市、自治区
CH_PROV = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
           '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门']

# 所有的地级以上城市
ALL_CH_CITY = ['北京', '天津', '沈阳', '长春', '哈尔滨', '上海', '南京', '武汉', '广州', '重庆', '成都', '西安', '石家庄', '唐山', '太原', '包头', '大连',
               '鞍山', '抚顺', '吉林', '齐齐哈尔', '徐州', '杭州', '福州', '南昌', '济南', '青岛', '淄博', '郑州', '长沙', '贵阳', '昆明', '兰州', '乌鲁木齐',
               '邯郸', '保定', '张家口', '大同', '呼和浩特', '本溪', '丹东', '锦州', '阜新', '辽阳', '鸡西', '鹤岗', '大庆', '伊春', '佳木斯', '牡丹江',
               '无锡', '常州', '苏州', '宁波', '合肥', '淮南', '淮北', '厦门', '枣庄', '烟台', '潍坊', '泰安', '临沂', '开封', '洛阳', '平顶山', '安阳',
               '新乡', '焦作', '黄石', '襄樊', '荆州', '株洲', '湘潭', '衡阳', '深圳', '汕头', '湛江', '南宁', '柳州', '西宁', '秦皇岛', '邢台', '承德',
               '沧州', '廊坊', '衡水', '阳泉', '长治', '乌海', '赤峰', '营口', '盘锦', '铁岭', '朝阳', '葫芦岛', '四平', '辽源', '通化', '白山', '松原',
               '白城', '双鸭山', '七台河', '南通', '连云港', '淮阴', '盐城', '扬州', '镇江', '泰州', '温州', '嘉兴', '湖州', '绍兴', '台州', '芜湖', '蚌埠',
               '马鞍山', '铜陵', '安庆', '阜阳', '泉州', '漳州', '南平', '龙岩', '景德镇', '萍乡', '九江', '新余', '东营', '济宁', '威海', '日照', '莱芜',
               '德州', '鹤壁', '濮阳', '许昌', '漯河', '南阳', '商丘', '十堰', '宜昌', '鄂州', '荆门', '孝感', '黄冈', '邵阳', '岳阳', '常德', '益阳',
               '郴州', '永州', '怀化', '韶关', '珠海', '佛山', '江门', '茂名', '肇庆', '惠州', '梅州', '阳江', '东莞', '中山', '潮州', '桂林', '梧州',
               '贵港', '海口', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '宜宾', '六盘水', '遵义', '曲靖', '铜川',
               '宝鸡', '咸阳', '汉中', '白银', '天水', '银川', '石嘴山', '克拉玛依', '晋城', '朔州', '通辽', '黑河', '宿迁', '金华', '衢州', '舟山', '黄山',
               '滁州', '宿州', '巢湖', '六安', '莆田', '三明', '鹰潭', '赣州', '聊城', '三门峡', '信阳', '咸宁', '张家界', '娄底', '汕尾', '河源', '清远',
               '揭阳', '云浮', '北海', '防城港', '钦州', '玉林', '三亚', '达州', '玉溪', '渭南', '延安', '榆林', '嘉峪关', '金昌', '吴忠']


# 引入锁

# 查询所有的城市列表，把所有的城市汇总，去重后返回一个列表
def listAllCity():
    dict = {'a': 1}  ## 空字典
    list = [""]  ## 空列表
    for v in CH_PROV:
        dict[v] = 1
        list.append(v)
    for v in PROV_CITY:
        if v in dict:
            continue
        dict[v] = 1
        list.append(v)
    for v in GD_CITY:
        if v in dict:
            continue
        dict[v] = 1
        list.append(v)
    for v in ALL_CH_CITY:
        if v in dict:
            continue
        dict[v] = 1
        list.append(v)
    return list



CITY_LIST = None
# 引入锁
L = threading.Lock()


def __initCity_List():
    global CITY_LIST
    L.acquire()
    if CITY_LIST is None:
        CITY_LIST = listAllCity()
    pass
    L.release()


# 获取第一个querykey
def getFristCity():
    __initCity_List()
    return CITY_LIST[0]


# 获取下一个querykey
def getNextCity(city=None):
    __initCity_List()
    iseq = False
    for v in CITY_LIST:
        if iseq:
            return v
        if v == city:
            iseq = True
    pass
    return None


if __name__ == '__main__':
    list = listAllCity()
    print(getNextCity(""))

