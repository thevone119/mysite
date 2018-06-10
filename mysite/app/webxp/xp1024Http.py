# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from mysite.libs import BaseHttpGet
from mysite.app.webxp import models

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

#网站的跟路径
xp_base_url="http://d2.sku117.info"
FILTER_COUNT=0 #过滤的总数
#抓取列表
class xp1024_list_crawer(BaseHttpGet.BaseHttpGet):
    url = None
    pub_type=None
    # 执行数据爬取前先设置headers
    def before(self):
        return True

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            print(time.strftime("%d %H:%M:%S", time.localtime(time.time())), "抓取网站(", self.url, ")开始-----")
            soup = BeautifulSoup(response.content.decode("utf-8", 'replace'), "lxml")
            trs = soup.find_all("tr", class_='tr3 t_one', align="center")
            for tr in trs:
                if (str(tr).find("置顶") > 0):
                    continue
                namelink = tr.find('h3').find('a')
                if namelink is None:
                    continue
                pub_id = namelink.get("id")
                mv = models.XP1024Movie.objects.filter(pub_id=pub_id).first()
                # 判断影片是否已经存在，如果存在，则不在进行下一步处理
                if mv is None:
                    mv = models.XP1024Movie()
                    mv.pub_src="1024xp"
                else:
                    continue
                mv.pub_type = self.pub_type
                mv.pub_day = tr.find('a', class_='f10').string.strip()
                mv.pub_name = namelink.string.strip()
                mv.pub_info_url = "/pw/" + namelink.get("href")
                mv.pub_id = pub_id
                catidx = mv.pub_name.find("] ")
                if catidx > 0:
                    mv.pub_name = mv.pub_name[catidx + 2:]


                # 抽取明细
                info = xp1024_info_crawer()
                info.mv=mv
                BaseHttpGet.pushHttpGet(info)


        except Exception as e:
            print("xp1024_list_crawer数据解析出错:", e)
            return False
        return True
        pass

#抓取明细
class xp1024_info_crawer(BaseHttpGet.BaseHttpGet):
    url = None
    mv=None
    err_count=0 #错误次数 ，连续错误2次就退出
    # 执行数据爬取前先设置headers
    def before(self):
        self.url = xp_base_url + self.mv.pub_info_url
        #错误超过2次，直接作废
        if self.err_count>2:
            return False
        return True

    # 这个方法由子类实现，爬虫爬取完成后，会调用此方法
    # 如果这个返回True，则代表调用成功，移除出调用列表
    # 如果这个返回False,则代表调用失败，重新加入调用列表
    def parse(self, response):
        try:
            global FILTER_COUNT
            print("解析资源", self.mv.pub_info_url)
            html = response.content.decode("utf-8", 'replace')
            soup = BeautifulSoup(html, "lxml")
            div = soup.find("div", id="read_tpc")
            divtext = str(div)
            #print(divtext)
            cstart = divtext.find("read_tpc\">")

            if(cstart<0):
                cstart = divtext.find("名稱】")
            else:
                cstart=cstart+len("read_tpc\">")

            cend = divtext.find("<img",cstart)
            cend2 =  divtext.find("<a",cstart)
            if cend2>0 and cend2<cend:
                cend=cend2
            if(cend>500):
                cend=500
            if (cstart > 0 and cend > cstart):
                self.mv.pub_content = divtext[cstart:cend]
            # 图片地址
            imgs = div.find_all("img")
            if (len(imgs) > 0):
                self.mv.pub_img_url = imgs[0].get("src")
            # 下载地址
            links = div.find_all("a")
            for a in links:
                link = a.get("href")
                if (link.find("torrent") > 0):
                    self.mv.pub_down_url = link
            # 如果图片小于50K则过滤掉
            if(len(self.mv.pub_img_url)<5):
                print("影片没有图片，获取失败", self.mv.pub_img_url, self.mv.pub_info_url, FILTER_COUNT)
                return True

            imgsize = getRemoteFileSize(self.mv.pub_img_url)
            if imgsize ==0 :
                print("影片的图片获取失败，资源可能已失效", self.mv.pub_img_url, self.mv.pub_info_url, FILTER_COUNT)
                self.err_count = self.err_count + 1
                return False
            self.mv.pub_img_size=imgsize


            #读取下一个
            if(query_xp_torrent(self.mv)):
                #解析种子成功，则保存
                self.mv.save()
            else:
                print("获取下载种子地址失败", self.mv.pub_down_url, self.mv.pub_info_url, FILTER_COUNT)
                self.err_count = self.err_count + 1
                return False

        except Exception as e:
            print("xp1024_info_crawer数据解析出错:", e,self.mv.__dict__)
            self.err_count = self.err_count+1
            return False
        return True
        pass


def getRemoteFileSize(url):
    """ 通过content-length头获取远程文件大小
        url - 目标文件URL
        """
    if url is None or len(url)<5:
        return 0
    try:
        r=BaseHttpGet.getSessionPool().get(url, headers=headers)
        return len(r.content)
    except Exception as e: # 远程文件不存在
        return 0


#查询下载链接
def query_xp_torrent(mv=None):
    r = BaseHttpGet.getSessionPool().get(mv.pub_down_url, headers=headers)
    html = r.content.decode("utf-8", 'replace')
    soup = BeautifulSoup(html, "lxml")
    links=soup.find_all("a")
    for a in links:
        link = a.get("href")
        if(link.find("magnet:")!=-1):
            mv.pub_down_url = link
            return True
    pass
    return False
