
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.host, 'Origin': self.host, 'Connection': 'keep-alive'
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
        {"type_id": "20", "type_name": "最新"},
        {"type_id": "21", "type_name": "最佳"},
        {"type_id": "22", "type_name": "热门"},
        {"type_id": "24", "type_name": "24日无码"},
        {"type_id": "27", "type_name": "27性感"},
        {"type_id": "28", "type_name": "28乱"},
        {"type_id": "29", "type_name": "29欧美"},
        {"type_id": "29", "type_name": "31三级"},
        {"type_id": "29", "type_name": "32卡通"},
        {"type_id": "29", "type_name": "33"},
        {"type_id": "29", "type_name": "35"}
                            ],
                 }
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        tag = tid
        urlstr=f'?pg={pg}&t={tag}' if int(pg)>1 else f'?t={tag}'
        data = self.getjson(self.host+'/api/json.php'+urlstr)
        videos = []
        pagecount=data["pagecount"]
        limit=data["limit"]
        total=data["total"]
        arr=data["list"]
        for item in arr:
            vod_id = item["vod_play_url"]
            videos.append({
                "vod_id": vod_id,
                "vod_name": item["vod_name"],
                "vod_pic": item["vod_pic"],
                "vod_remarks": item["vod_id"]
            })
        '''videos.append({
            "vod_id": "https://video17.balecao.com/video/20220227/e0f64dfe84cbfe8c1367dfba2c689afd/index.m3u8",
            "vod_name": "",
            "vod_pic": "https://www.baidu.com/img/flexible/logo/pc/result.png",
            "vod_remarks": ""
        })'''
        return {
            "list": videos,
            "page": pg,
            "pagecount": pagecount,
            "limit": limit,
            "total": total
        }

    def detailContent(self, array):
        url = array[0]
        vod = {
            "vod_play_from": "线路",
            "vod_play_url": f"正片${url}"
        }
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        pass

    def playerContent(self, flag, id, vipFlags):
        return {
            "url": id,
            "parse": '0',
            "contentType": '',
            "header": self.headers
        }

    def getjson(self, path):
        rsp = self.session.get(f'{path}', timeout=5)
        return rsp.json()
          
    def getpq(self, path):
        try:
            rsp = self.session.get(f'{path}', timeout=5).text
            return pq(rsp.encode('utf-8'))
        except Exception as e:
            print(f"请求失败: , {str(e)}")
            return None
    

