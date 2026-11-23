
# coding=utf-8
# !/usr/bin/python
import sys
import requests
import re
import base64
import json
from requests import Session
from base.spider import Spider
from pyquery import PyQuery as pq
from urllib.parse import quote, unquote,urljoin
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
sys.path.append('..') 

class Spider(Spider):
    def init(self, extend="{}"):
        self.host = "https://www.gdlsp.com"
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
        {"type_id": "categories/pantyhose", "type_name": "Pantyhose"}
                            ],
                 }
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        tag = tid
        urlstr=f'?pg={pg}' if int(pg)>1 else ''
        data = self.getjson(self.host+'/api/json.php'+urlstr)
        return {
            "page": data.get("page", 1),
            "pagecount": data.get("pagecount", 9),
            "limit": data.get("limit", 20),
            "total": data.get("total", 99),
            "list": data.get("list", [])
        }

    def getPicS(self,picurl):
        if not picurl:
            return ""
        return picurl.replace('medium@2x','small')

    def detailContent(self, array):
        # array[0] = csp返回的vod_id
        vod_id = array[0]
        return vod_id

    def searchContent(self, key, quick, pg="1"):
        pass

    def playerContent(self, flag, id, vipFlags):
        return {
            "url": id,
            "parse": '0',
            "contentType": '',
            "header": self.headers
        }

    def localProxy(self, param):
        if param['type'] == 'img':
            content = self.decrypt_img(unquote(param['url']))
            return [200, "application/octet-stream", content]

    def getjson(self, path):
        try:
            rsp = self.session.get(f'{path}', timeout=5).text
            return rsp.json()
        except Exception as e:
            print(f"请求失败: , {str(e)}")
            return None
          
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
        return img_url
        """
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
"""

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

