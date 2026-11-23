
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
        videos = []
        arr=data.get("list", [])
        for item in arr:
            vod_id = item.get("vod_play_url")
            if not vod_id
                continue
            videos.append({
                "vod_id": vod_id,
                "vod_name": item.get("vod_name",""),
                "vod_pic": item.get("vod_pic",""),
                "vod_remarks": item.get("vod_time","")
            })
        return {
            "list": videos,
            "page": pg,
            "pagecount": item.get("pagecount",""),
            "limit": item.get("limit",""),
            "total": item.get("total","")
        }

    def getPicS(self,picurl):
        if not picurl:
            return ""
        return picurl.replace('medium@2x','small')

    def detailContent(self, array):
        url = array[0]
        return {
            "vod_play_from": "线路",
            "vod_play_url": f"$${url}"
        }

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
    

