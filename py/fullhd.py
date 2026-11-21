
# coding=utf-8
# !/usr/bin/python
import sys
import requests
import re
import base64
from requests import Session
from base.spider import Spider
from pyquery import PyQuery as pq
from urllib.parse import quote, unquote,urljoin
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
sys.path.append('..') 

class Spider(Spider):
    def init(self, extend="{}"):
        self.host = "https://www.fullhd.to"
        self.headers = {
            'Referer': self.host,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
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
        urlstr=f'/{tag}/{pg}' if int(pg)>1 else f'/{tag}/'
        rsp = self.getpq(self.host+urlstr)
        videos = self.parseVodList(rsp)
        limit = 30
        total = 99999
        return {
            "list": videos,
            "page": pg,
            "pagecount": (total + limit - 1) // limit,
            "limit": limit,
            "total": total
        }
    def parseVodList(self, rsp):
    #"""公共函数：从pyquery rsp对象提取vod列表，categoryContent、searchContent共用"""
        videos = []
        for item in rsp('a.thumb_img').items():
            href = item.attr('href')
            if href is None:
                continue
            img_src=self.buildImgUrl(href)
            text = item.attr('title')
            text = text.strip() if text else ""
            #img_src = item.find('img').attr('data-src')
            #if img_src is None or img_src == '':
            #    img_src = item.find('img').attr('src')
            duration = item.find('span.duration').text()
            duration = duration.strip() if duration else ""

            videos.append({
                "vod_id": href,
                "vod_name": text,
                "vod_pic": self.getPicS(img_src),
                "vod_remarks": duration
            })
        return videos

    def getPicS(self,picurl):
        if not picurl:
            return ""
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
            label = s.attr("label") or ""
            src = s.attr("src") or ""
            if not label.strip() or not src.strip():
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
    
        # ✅ 按 weight【从小到大排序】！！如果你想要从高到低：source_list.sort(key=lambda x:x["weight"], reverse=True)
        source_list.sort(key=lambda x: x["weight"])
        # ============ 重点：仿照范例，构造多线路字符串，使用 $$$ 作为线路分隔符 ============
        names = []     # 线路名称列表（清晰度）
        play_lines = []# 每一条线路对应的剧集字符串
        for item in source_list:
            names.append(item["label"])
            # 当前线路只有单集，数组内仅一条，#join之后就是这一集
            one_ep = [f"播放${quote(item['src'])}"]
            play_lines.append("#".join(one_ep))
    
        vod_play_from = "$$$".join(names)
        vod_play_url  = "$$$".join(play_lines)
    
        # 组装vod对象
        vod = {
            "vod_id": detail_url,
            "vod_name": "暂无名称",
            "vod_pic": "",  # 后续接入 buildImgUrl
            "vod_play_from": vod_play_from,
            "vod_play_url": vod_play_url
        }
        return {"list": [vod]}



    def searchContent(self, key, quick, pg="1"):
        urlstr=f'/{pg}' if int(pg)>1 else f''
        rsp = self.getpq(self.host+f'search/{quote(key)}/'+urlstr)
        videos = self.parseVodList(rsp)
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
    
    def buildImgUrl(self, detail_url):
        """
        从详情页url提取vid拼接图片地址；
        如果需要，下载图片转为base64图片data-url
        return: 正常返回base64图片串，出错返回 ""
        """
        # 提取 /videos/后面的数字id
        m = re.search(r'/videos/(\d+)', detail_url)
        if not m:
            return ""
        vid_str = m.group(1)
        try:
            vid = int(vid_str)
        except ValueError:
            return ""
        group_id = vid - (vid % 1000)  # 后三位清零
        img_url = f"https://img.fullhd.to/{group_id}/{vid}/small/1.jpg"
#https://down.nigx.cn/raw.githubusercontent.com/wsonline2008/tvbox/refs/heads/master/188X.json
        
        # ========== 新增：下载图片 + base64编码 ==========
        try:
            # 这里替换成你项目统一的http请求！！如果你的项目不用self.session就改成你自己的get函数
            resp = self.session.get(img_url, timeout=5)
            resp.raise_for_status()  # 4xx/5xx直接抛异常进入except
            img_bytes = resp.content
            if not img_bytes:
                return ""
            # 二进制转base64
            b64_data = base64.b64encode(img_bytes).decode("utf-8")
            # 组装成浏览器可识别的data url
            img_base64 = f"data:image/jpeg;base64,{b64_data}"
            return img_base64
        except Exception as e:
            # 图片请求失败（超时、403、404、防盗链）直接返回空字符串
            # 你可以在这里print调试：print("图片获取失败", img_url, e)
            return ""


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
