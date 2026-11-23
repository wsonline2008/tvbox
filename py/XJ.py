# coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
import time
import urllib.parse
import re
import requests
from lxml import etree
from urllib.parse import urljoin

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
        # 定义特殊分区ID列表，包含所有需要特殊处理的分类
        self.special_categories = ['13', '14', '33',  '53', '32', '52', '9']
        self.log(f"苹果爬虫初始化完成，主站: {self.host}")

    def html(self, content):
        """将HTML内容转换为可查询的对象"""
        try:
            return etree.HTML(content)
        except:
            self.log("HTML解析失败")
            return None

    def regStr(self, pattern, string, index=1):
        """正则表达式提取字符串"""
        try:
            match = re.search(pattern, string, re.IGNORECASE)
            if match and len(match.groups()) >= index:
                return match.group(index)
        except:
            pass
        return ""

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        """获取首页内容和分类"""
        result = {}
        # 只保留指定的分类
        classes = [
            {'type_id': '618041.xyz_1', 'type_name': '全部视频'},
            {'type_id': '618041.xyz_13', 'type_name': '香蕉精品'},
            {'type_id': '618041.xyz_22', 'type_name': '制服诱惑'},
            {'type_id': '618041.xyz_6', 'type_name': '国产视频'},
            {'type_id': '618041.xyz_8', 'type_name': '清纯少女'},
            {'type_id': '618041.xyz_9', 'type_name': '辣妹大奶'},
            {'type_id': '618041.xyz_10', 'type_name': '女同专属'},
            {'type_id': '618041.xyz_11', 'type_name': '素人出演'},
            {'type_id': '618041.xyz_12', 'type_name': '角色扮演'},
            {'type_id': '618041.xyz_20', 'type_name': '人妻熟女'},
            {'type_id': '618041.xyz_23', 'type_name': '日韩剧情'},
            {'type_id': '618041.xyz_21', 'type_name': '经典伦理'},
            {'type_id': '618041.xyz_7', 'type_name': '成人动漫'},
            {'type_id': '618041.xyz_14', 'type_name': '精品二区'},
            {'type_id': '618041.xyz_53', 'type_name': '动漫中字'},
            {'type_id': '618041.xyz_52', 'type_name': '日本无码'},
            {'type_id': '618041.xyz_33', 'type_name': '中文字幕'},
            {'type_id': '618041.xyz_32', 'type_name': '国产自拍'}
        ]
        result['class'] = classes
        try:
            rsp = self.fetch(self.host, headers=self.headers)
            doc = self.html(rsp.text)
            videos = self._get_videos(doc, limit=20)
            result['list'] = videos
        except Exception as e:
            self.log(f"首页获取出错: {str(e)}")
            result['list'] = []
        return result

    def homeVideoContent(self):
        """分类定义 - 兼容性方法"""
        return {
            'class': [
                {'type_id': '618041.xyz_1', 'type_name': '全部视频'},
                {'type_id': '618041.xyz_13', 'type_name': '香蕉精品'},
                {'type_id': '618041.xyz_22', 'type_name': '制服诱惑'},
                {'type_id': '618041.xyz_6', 'type_name': '国产视频'},
                {'type_id': '618041.xyz_8', 'type_name': '清纯少女'},
                {'type_id': '618041.xyz_9', 'type_name': '辣妹大奶'},
                {'type_id': '618041.xyz_10', 'type_name': '女同专属'},
                {'type_id': '618041.xyz_11', 'type_name': '素人出演'},
                {'type_id': '618041.xyz_12', 'type_name': '角色扮演'},
                {'type_id': '618041.xyz_20', 'type_name': '人妻熟女'},
                {'type_id': '618041.xyz_23', 'type_name': '日韩剧情'},
                {'type_id': '618041.xyz_21', 'type_name': '经典伦理'},
                {'type_id': '618041.xyz_7', 'type_name': '成人动漫'},
                {'type_id': '618041.xyz_14', 'type_name': '精品二区'},
                {'type_id': '618041.xyz_53', 'type_name': '动漫中字'},
                {'type_id': '618041.xyz_52', 'type_name': '日本无码'},
                {'type_id': '618041.xyz_33', 'type_name': '中文字幕'},
                {'type_id': '618041.xyz_32', 'type_name': '国产自拍'}
            ]
        }

    def categoryContent(self, tid, pg, filter, extend):
        """分类内容 - 修改为使用固定页数设置"""
        try:
            domain, type_id = tid.split('_')
            url = f"https://{domain}/index.php/vod/type/id/{type_id}.html"
            if pg and pg != '1':
                url = url.replace('.html', f'/page/{pg}.html')
            # 在这里将 type_id 传递给 _get_videos 方法
            videos = self._get_videos(url, category_id=type_id, limit=20)
            
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
            self.log(f"分类内容获取出错: {str(e)}")
            return {'list': []}

    def searchContent(self, key, quick, pg="1"):
        """搜索功能 - 完全修复版"""
        try:
            # 构造搜索URL
            search_url = f"{self.host}/index.php/vod/type/id/1/wd/{urllib.parse.quote(key)}/page/{pg}.html"
            self.log(f"搜索URL: {search_url}")
            
            # 提取搜索结果
            videos = self._get_videos(search_url, limit=20)
            
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
            self.log(f"搜索出错: {str(e)}")
            return {'list': []}

    def detailContent(self, array):
        play_url = array[0]
        return {
            "vod_play_from": "线路1",
            "vod_play_url": f"$${play_url}"
        }

    def playerContent(self, flag, id, vipFlags):
        return {
            "url": id,
            "parse": '0',
            "contentType": '',
            "header": self.headers
        }

    def _get_videos(self, url, category_id=None, limit=None):
        """获取列表 - 根据实际网站结构"""
        try:
            rsp = self.fetch(url, headers=self.headers)
            doc = self.html(rsp.text)
            videos = []
            elements = doc.xpath('//a[@class="vodbox"]')
            for elem in elements:
                link = elem.xpath('./@href')[0]
                if link.startswith('/'):
                    link = self.host + link
                # 提取链接中的参数
                parsed_url = urllib.parse.urlparse(link)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                href = query_params.get('v', [''])[0]
                img_src = query_params.get('b', [''])[0]
                # 提取标题
                title_elem = element.xpath('.//p[@class="km-script"]/text()')
                if title_elem:
                    title_encrypted = title_elem[0].strip()
                    title_elem = self._decrypt_title(title_encrypted)
                else
                    title_elem = ''
                videos.append({
                    "vod_id": href,
                    "vod_name": title_elem,
                    "vod_pic": self.getPicS(img_src),
                    "vod_remarks": ''
                })
            return videos
        except Exception as e:
            self.log(f"获取影片列表出错: {str(e)}")
            return []

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
            self.log(f"标题解密失败: {str(e)}")
            return encrypted_text


    def _get_text(self, doc, selectors):
        """通用文本提取"""
        for selector in selectors:
            try:
                texts = doc.xpath(selector)
                for text in texts:
                    if text and text.strip():
                        return text.strip()
            except:
                continue
        return ''

    def log(self, message):
        """日志输出"""
        print(f"[video] {message}")

    def fetch(self, url, headers=None, method='GET', data=None, timeout=10):
        """网络请求"""
        try:
            if headers is None:
                headers = self.headers
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
            else:
                response = requests.post(url, headers=headers, data=data, timeout=timeout, verify=False)
            return response
        except Exception as e:
            self.log(f"网络请求失败: {url}, 错误: {str(e)}")
            return None

# 注册爬虫
if __name__ == '__main__':
    from base.spider import Spider as BaseSpider
    BaseSpider.register(Spider())
