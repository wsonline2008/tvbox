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
sys.path.append("..")

class Spider(Spider):
    
    def getName(self):
        return "苹果"
    #https://618420.xyz
    def init(self, extend=""):
        self.host = "https://618041.xyz"
        self.api_host = "https://h5.xxoo168.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': self.host
        }
        self.session = Session()
        self.session.headers.update(self.headers)
        # 定义特殊分区ID列表，包含所有需要特殊处理的分类
        self.special_categories = ['13', '14', '33',  '53', '32', '52', '9']

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        """获取首页内容和分类"""
        result = {}
        # 只保留指定的分类
        classes = [
            #{'type_id': '1', 'type_name': '全部视频'},
            {'type_id': '13', 'type_name': '香蕉精品'},
            {'type_id': '22', 'type_name': '制服诱惑'},
            {'type_id': '6', 'type_name': '国产视频'},
            {'type_id': '8', 'type_name': '清纯少女'},
            {'type_id': '9', 'type_name': '辣妹大奶'},
            {'type_id': '10', 'type_name': '女同专属'},
            {'type_id': '11', 'type_name': '素人出演'},
            {'type_id': '12', 'type_name': '角色扮演'},
            {'type_id': '20', 'type_name': '人妻熟女'},
            {'type_id': '23', 'type_name': '日韩剧情'},
            {'type_id': '21', 'type_name': '经典伦理'},
            {'type_id': '7', 'type_name': '成人动漫'},
            {'type_id': '14', 'type_name': '精品二区'},
            {'type_id': '53', 'type_name': '动漫中字'},
            {'type_id': '52', 'type_name': '日本无码'},
            {'type_id': '33', 'type_name': '中文字幕'},
            {'type_id': '32', 'type_name': '国产自拍'}
        ]
        result['class'] = classes
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容 - 修改为使用固定页数设置"""
        try:
            #domain, type_id = tid.split('_')
            url = f"{self.host}/index.php/vod/type/id/{tid}.html"
            if pg and pg != '1':
                url = url.replace('.html', f'/page/{pg}.html')
            # 在这里将 type_id 传递给 _get_videos 方法
            videos = self.parseVodList(url)
            # 使用固定页数设置，而不是尝试从页面解析
            pagecount = 999
            total = 19980
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 20,
                'total': total
            }
        except Exception as e:
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        """搜索功能 - 完全修复版"""
        try:
            # 构造搜索URL
            search_url = f"{self.host}/index.php/vod/type/id/1/wd/{urllib.parse.quote(key)}/page/{pg}.html"
            # 提取搜索结果
            videos = self.parseVodList(search_url)
            # 使用固定页数设置，而不是尝试从页面解析
            pagecount = 999
            total = 19980
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': pagecount,
                'limit': 20,
                'total': total
            }
        except Exception as e:
            return {'list': []}

    def detailContent(self, array):
        play_url = array[0]
        return {
            "vod_play_from": "线路1",
            "vod_play_url": f"正片${play_url}"
        }

    def playerContent(self, flag, id, vipFlags):
        return {
            "url": id,
            "parse": '0',
            "contentType": '',
            "header": self.headers
        }

    def _decrypt_title(self, encrypted_text):
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

    def parseVodList(self, url):
    #"""公共函数：从pyquery rsp对象提取vod列表，categoryContent、searchContent共用"""
        rsp = self.getpq(url)
        videos = []
        Aitems=rsp('a.vodbox').items()
        if not Aitems
            Aitems=rsp('a.thumbnail').items()
        for item in Aitems:
            link = item.attr('href')
            if link is None:
                continue
            # 提取链接中的参数
            parsed_url = urllib.parse.urlparse(link)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            href = query_params.get('v', [''])[0]
            img_src = query_params.get('b', [''])[0]
            # 提取标题
            title_elem = item.find('p.km-script').text()
            if title_elem:
                title_encrypted = title_elem.strip()
                title_elem = self._decrypt_title(title_encrypted)
            else
                title_elem = ''

            videos.append({
                "vod_id": href,
                "vod_name": title_elem,
                "vod_pic": img_src,
                "vod_remarks": ''
            })
        return videos

    def getpq(self, path):
        try:
            rsp = self.session.get(f'{path}', timeout=5).text
            return pq(rsp.encode('utf-8'))
        except Exception as e:
            print(f"请求失败: , {str(e)}")
            return None

    def parseVodList2(self, url):
    #"""公共函数：从pyquery rsp对象提取vod列表，categoryContent、searchContent共用"""9o8qTJso6c53V89mrWScFo1ncht2fvatitCVJYoj2tb8egCxgRQJu42PZxjaL711U4
        rsp = self.getpq(url)
        videos = []
        videos.append({
            "vod_id": 'https://m-hs.cqvelf.cn/20250731/ekrbYkY2z/vXsk5vmrCBv/LpMgv9HL/index.m3u8',
            "vod_name": 'a',
            "vod_pic": '',
            "vod_remarks": ''
        })
        return videos
