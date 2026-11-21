
# coding=utf-8
# !/usr/bin/python
import sys
import requests
from requests import Session
from base.spider import Spider
from pyquery import PyQuery as pq
from urllib.parse import quote, unquote
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
sys.path.append('..') 

class Spider(Spider):
    def init(self, extend="{}"):
        self.host = "https://www.fullhd.to"
        self.headers = {
            'Referer': self.host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0'
        }
        self.session = Session()
        self.session.headers.update(self.headers)

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass
    def homeContent(self, filter):
        result = {}
        result = {"class": [
        {"type_id": "latest-updates", "type_name": "最新"},
        {"type_id": "top-rated", "type_name": "最佳"},
        {"type_id": "most-popular", "type_name": "热门"},
        {"type_id": "networks/brazzers-com", "type_name": "Brazzers"},
        {"type_id": "networks/tushy-com", "type_name": "Tushy"},
        {"type_id": "networks/naughtyamerica-com", "type_name": "Naughtyamerica"},
        {"type_id": "sites/sexmex", "type_name": "Sexmex"},
        {"type_id": "sites/passion-hd", "type_name": "Passion"},
        {"type_id": "categories/animation", "type_name": "动画"},
        {"type_id": "categories/18-years-old", "type_name": "18岁"},
        {"type_id": "categories/pawg", "type_name": "美臀"},
        {"type_id": "categories/thong", "type_name": "丁字裤"},
        {"type_id": "categories/stockings", "type_name": "丝袜"},
        {"type_id": "categories/jav-uncensored", "type_name": "日本"},
        {"type_id": "categories/pantyhose", "type_name": "Pantyhose"}
                            ],
                 }
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        tag = tid
        urlstr=f'/{tag}/{pg}' if pg>1 else f'/{tag}/'
        rsp = self.getpq(self.host+urlstr)
        videos = []
        for item in rsp('a.thumb_img').items():
            href = item.attr('href')
            text = item.attr('title').strip()
            img_src = item.find('img').attr('data-src')
            if img_src=='':
                img_src=item.find('img').attr('src')
            duration = item.find('span.duration').text().strip()
            videos.append({
                "vod_id": href,
                "vod_name": text,
                "vod_pic": self.getPicS(img_src),#//f"{self.getProxyUrl()}&type=img&url={quote(img_src)}",
                "vod_remarks": duration
            })
        #//pager = rsp('ul.pager.dx-pager')
        limit = 30
        total = 99999
        return {
            "list": videos,
            "page": pg,
            "pagecount": (total + limit - 1) // limit,
            "limit": limit,
            "total": total
        }
    def getPicS(picurl):
        return picurl.replace('medium@2x','small')

    def detailContent(self, array):
        # array[0] 就是传过来的详情页url（沿用咱们前面约定：vod_id存详情页链接）
        detail_url = array[0]
        rsp = self.getpq(detail_url)
        # 👉 取出所有 source 标签
        source_items = rsp("video source").items()
        # ========== 清晰度权重表【从小到大！！数字越小清晰度越低】你可以自行扩充修改 ==========
        rank_map = {
            "360P": 1,
            "480P": 2,
            "720P": 3,
            "1080P": 4,
            "2160P": 6,
            "2K": 8,
            "4K": 10
        }
        source_list = []
        for s in source_items:
            label = s.attr("label")
            src = s.attr("src")
            if not label or not src:
                continue  # label或者src为空直接跳过这条无效source
            # 补全相对路径为完整url
            full_src = urljoin(detail_url, src)
            # 获取排序权重，如果label不在rank_map里面，默认给一个比较大的值放到末尾
            weight = rank_map.get(label.upper(), 99)
            source_list.append({
                "label": label,
                "src": full_src,
                "weight": weight
            })
    
        # ✅ 按 weight【从小到大排序】！！
        source_list.sort(key=lambda x: x["weight"])
    
        # 拼接成 CSP 多选集字符串： label$url#label$url#...
        play_parts = []
        for item in source_list:
            play_parts.append(f"{item['label']}${quote(item['src'])}")
        vod_play_url = "#".join(play_parts)
    
        # 组装vod对象，线路名称你自行修改，这里写"多清晰度"
        vod = {
            "vod_id": detail_url,
            "vod_name": "",
            "vod_pic": "", # 海报有就填，需要代理就套 self.getProxyUrl()+quote
            "vod_play_from": "多清晰度",
            "vod_play_url": vod_play_url
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        urlstr=f'/{pg}' if pg>1 else f''
        rsp = self.getpq(self.host+f'search/{quote(key)}/'+urlstr)
        videos = []
        for item in rsp('a.thumb_img').items():
            href = item.attr('href')
            text = item.attr('title').strip()
            img_src = item.find('img').attr('data-src')
            if img_src=='':
                img_src=item.find('img').attr('src')
            duration = item.find('span.duration').text().strip()
            videos.append({
                "vod_id": href,
                "vod_name": text,
                "vod_pic": self.getPicS(img_src),#//f"{self.getProxyUrl()}&type=img&url={quote(img_src)}",
                "vod_remarks": duration
            })
        #//pager = rsp('ul.pager.dx-pager')
        limit = 30
        total = 99999
        return {
            "list": videos,
            "page": pg,
            "pagecount": (total + limit - 1) // limit,
            "limit": limit,
            "total": total
        }

    def playerContent(self, flag, id, vipFlags):
        return {
            "url": unquote(id),
            "parse": '0',
            "contentType": '',
            "header": self.headers
        }

    def localProxy(self, param):
        if param['type'] == 'img':
            content = self.decrypt_img(unquote(param['url']))
            return [200, "application/octet-stream", content]

    def getpq(self, path):
        try:
            rsp = self.session.get(f'{path}', timeout=5).text
            return pq(rsp.encode('utf-8'))
        except Exception as e:
            print(f"请求失败: , {str(e)}")
            return None
    
    def decrypt_img(self, url):
        key_str = 'f5d965df75336270'
        iv_str = '97b60394abc2fbe1'
        key = key_str.encode('utf-8')
        iv = iv_str.encode('utf-8')
        encrypted_bytes = self.session.get(url, timeout=5).content
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        final_data = unpad(decrypted_bytes, AES.block_size)
        return final_data
