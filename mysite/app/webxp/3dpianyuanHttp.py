# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from mysite.libs import BaseHttpGet
from mysite.app.webxp import models

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }


BASE_URL="http://www.3dpianyuan.net/"

# 执行数据爬取前先设置headers
myheaders={"Cookie":"__guid=177923619.1069204886338590600.1526320086937.1675; _uab_collina=152632008723128978128677; UM_distinctid=1635fc44152282-04f257fd65d9fc-6b1b1279-1fa400-1635fc441536e; WgxE_2132_pc_size_c=0; WgxE_2132_saltkey=VOGr4O87; WgxE_2132_lastvisit=1528704412; _umdata=0712F33290AB8A6D0E461F982592EEC8C85EBAB65E0ED4E494744BB5557C3E0CBE57548D7E92AEABCD43AD3E795C914CC25385DC496FF5D9D348B31CF9FDCAE7; WgxE_2132_ulastactivity=1528708194%7C0; WgxE_2132_auth=e2eeeprWv8nV6JbzVh3Sb%2BqwkLuQP6Au5lqgEr0ZId5PNRu2X%2BPT0yUL546ZeEc0ALSjtHkxEwS7aX%2F6tBueO8FRUPc; WgxE_2132_lastcheckfeed=246169%7C1528708194; WgxE_2132_visitedfid=2D41; WgxE_2132_viewid=tid_1014; monitor_count=15; CNZZDATA4991241=cnzz_eid%3D425150996-1526318445-null%26ntime%3D1528703868; WgxE_2132_smile=1D1; WgxE_2132_lastact=1528709027%09forum.php%09ajax"}

#抓取列表
class pianyuan_list_crawer(BaseHttpGet.BaseHttpGet):
    url = None
    pub_type=None
    def before(self):
        global myheaders
        #先要设置cookie哦。
        self.headers=myheaders
        return True

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            global BASE_URL
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取网站(", self.url, ")开始-----")
            html=response.content.decode("gbk", 'replace')
            #print(html)
            soup = BeautifulSoup(html, "lxml")
            links = soup.find_all("a", class_='xst')
            for link in links:
                lurl = link.get("href")
                if lurl is None:
                    continue
                if len(lurl)<5:
                    continue
                pub_id=lurl
                lurl=BASE_URL+lurl
                mv = models.XP1024Movie.objects.filter(pub_id=pub_id).first()
                # 判断影片是否已经存在，如果存在，则不在进行下一步处理
                if mv is None:
                    mv = models.XP1024Movie()
                    mv.pub_src = "www.3dpianyuan.net"
                else:
                    continue

                mv.pub_type = self.pub_type

                mv.pub_name = link.string
                mv.pub_info_url = lurl
                mv.pub_id = pub_id
                query_pianyuan_info(mv)
                print(mv.__dict__)
        except Exception as e:
            print("pianyuan_list_crawer数据解析出错:", e)
            raise e
            return False
        return True
        pass



# 查询明细
def query_pianyuan_info(mv=None):
    global myheaders
    r = BaseHttpGet.getSessionPool().get(mv.pub_info_url, headers=myheaders, timeout=10)
    html = r.content.decode("gbk", 'replace')
    soup = BeautifulSoup(html, "lxml")
    hdiv = soup.find("div",class_="showhide")
    sidx = hdiv.text.find("magnet:")
    if sidx==-1:
        sidx = hdiv.text.find("http://gdl.lixian.vip.xunlei.com")
    if sidx==-1:
        print("下载地址无效",hdiv.text)
        return False

    mv.pub_down_url = hdiv.text[sidx:]
    if(len(mv.pub_down_url)>1000):
        print("下载地址无效2" ,len(mv.pub_down_url),mv.pub_down_url)
        return False
    td = hdiv.parent.parent
    links = td.find_all("a")

    for link in links:
        href = link.get("href")
        if href is not None and href.find("thread-")>0:
            mv.pub_font_url=href
            break
    if mv.pub_font_url is None:
        #没有字幕，直接保存
        mv.save()
        return False
    else:
        query_pianyuan_font(mv)
    pass
    return True

# 查询字幕，保存到D:/ZIMU/目录下
def query_pianyuan_font(mv=None):
    global myheaders,BASE_URL
    r = BaseHttpGet.getSessionPool().get(mv.pub_font_url, headers=myheaders, timeout=10)
    html = r.content.decode("gbk", 'replace')
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a")

    font_name=None
    down_url=None
    for link in links:
        href = link.get("href")
        if href is None or href.find("mod=attachment")==-1 :
            continue
        font_name = link.string
        if font_name is None or font_name.find("rar")==-1:
            continue
        down_url=href
    if down_url is None:
        print("字幕下载地址获取失败", down_url)
        return False
    pass
    #下载字幕哦
    dr = BaseHttpGet.getSessionPool().get(BASE_URL+down_url, headers=myheaders, stream=True)
    f = open("D:/temp/"+font_name, "wb")
    for chunk in dr.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    mv.save()

    return True




if __name__ == '__main__':
    print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "sched.start()")
    #sched.start()
    #update_prod_item_job()
    for i in range(1,14):
        crawer = pianyuan_list_crawer()
        crawer.url = "http://www.3dpianyuan.net/forum-3d-2-"+str(i)+".html"
        crawer.pub_type = "左右3D"
        crawer.run()


    #xp1024_search_job()
    pass