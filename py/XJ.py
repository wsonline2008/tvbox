
# coding=utf-8
# !/usr/bin/python
import sys
import requests
import re
import base64
from requests import Session
from base.spider import Spider
from pyquery import PyQuery as pq
from urllib.parse import quote, unquote,urljoin,urlparse,parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
sys.path.append('..') 

class Spider(Spider):
    def init(self, extend="{}"):
        self.host = "https://618041.xyz"
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
        {'type_id': '13', 'type_name': '香蕉精品'}
                            ],
                 }
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        tag = tid
        urlstr=f'/index.php/vod/type/id/{tag}/page/{pg}.html' if int(pg)>1 else f'/index.php/vod/type/id/{tag}.html'
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
        for item in rsp('a.vodbox').items():
            href = item.attr('href')
            if href is None:
                continue
            #img_src=self.buildImgUrl(href)
            parsed = urlparse(href)
            query_dict = parse_qs(parsed.query)
            v_val = query_dict.get("v", [None])[0]
            #text = item.attr('title')
            #text = text.strip() if text else ""
            img_src = item.find('img.lazy').attr('data-original')
            #if img_src is None or img_src == '':
            #    img_src = item.find('img').attr('src')
            text = item.find('p.km-script').text()
            text = text.strip() if text else ""
            text = self._decrypt_title(text)
            videos.append({
                "vod_id": v_val,
                "vod_name": text,
                "vod_pic": self.getPicS(img_src),
                "vod_remarks": ""
            })
        return videos

    def getPicS(self,picurl):
        if not picurl:
            return ""
        return picurl.replace('medium@2x','small')

    def detailContent(self, array):
        play_url = array[0]
        return {
            "vod_play_from": "线路1",
            "vod_play_url": f"播放${play_url}"
        }

    def searchContent(self, key, quick, pg="1"):
        urlstr=f'/page/{pg}.html' if int(pg)>1 else f'.html'
        rsp = self.getpq(self.host+f'/index.php/vod/type/wd/{quote(key)}'+urlstr)
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

    def decrypt_title(self, encrypted_text):
        """解密标题 - 使用网站的解密算法"""
        try:
            decrypted_chars = []
            for char in encrypted_text:
                code_point = ord(char)
                decrypted_code = code_point ^ 128
                decrypted_char = chr(decrypted_code)
                decrypted_chars.append(decrypted_char)
            
            decrypted_text = ''.join(decrypted_chars)
            return decrypted_text
        except Exception as e:
            return encrypted_text
