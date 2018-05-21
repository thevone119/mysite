# -*- coding: utf-8 -*-
#中国的省份，城市列表
import threading

#省会城市
PROV_CITY = ['太原','长春','南京','合肥','南昌','郑州','长沙','海口','贵阳','西安','西宁','呼和浩特','拉萨','乌鲁木齐','石家庄','沈阳','哈尔滨','杭州','福州','济南','广州','武汉','成都','昆明','兰州','台北','南宁','银川']

#广东城市
GD_CITY = ['广州','深圳','东莞','中山','珠海','汕头','佛山','韶关','湛江','肇庆','江门','茂名','惠州','梅州','汕尾','河源','阳江','清远','潮州','揭阳','云浮']

#省、直辖市、自治区
CH_PROV = ['北京','天津','上海','重庆','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆','香港','澳门']

# 引入锁

#查询所有的城市列表，把所有的城市汇总，去重后返回一个列表
def listAllCity():
    dict = {'a':1} ## 空字典
    list = []  ## 空列表
    for v in CH_PROV:
        dict[v]=1
        list.append(v)
    for v in PROV_CITY:
        if dict.get(v) is not None:
            continue
        dict[v]=1
        list.append(v)
    for v in GD_CITY:
        if dict.get(v) is not None:
            continue
        dict[v] = 1
        list.append(v)
    return list



if __name__ == '__main__':
    list = listAllCity()
    print(len(list))
    for i in list:
        print("call:", i)



