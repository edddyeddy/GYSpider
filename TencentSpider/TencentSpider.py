from Spider.Spider import *
from TencentSpider.tencentExtractor import *
import requests
import urllib.parse
import pymongo
import time
import json
import re


class TencentSpider(Spider):
    """
    腾讯公益爬虫
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum) -> list:
        """
        从项目列表页面获取项目id
        """
        print("TencentSpider don't support this method")
        return list()

    def _getRowData(self, projectID) -> dict:
        """
        获取原始数据
        """
        # 构造项目各类信息的URL
        proInfoUrl = 'https://ssl.gongyi.qq.com/cgi-bin/ProjInfoQuery.fcgi?jsoncallback=jQuery18305726600366653958_1609211876492&id=' + \
            str(projectID)+'&type=proj_base&_=' + \
            str(int(round(time.time() * 1000)))

        detailInfoUrl = 'https://scdn.gongyi.qq.com/json_data/data_detail/' + \
            str(projectID % 100)+'/detail.'+str(projectID)+'.js'

        progressInfoUrl = 'https://ssl.gongyi.qq.com/cgi-bin/WXUnprocessV2?pid=' + \
            str(projectID)+'&row=100&curr=1&jsoncallback=jQuery18309431007557373436_' + \
            str(int(round(time.time() * 1000)))

        rowData = {
            "detail": None,
            "pro": None,
            "progress": None
        }

        rowData['detail'] = self.__getJsInfo(detailInfoUrl)
        rowData['pro'] = self.__getJsInfo(proInfoUrl)
        rowData['progress'] = self.__getJsInfo(progressInfoUrl)

        return rowData

    def _extractData(self, rowData) -> dict:
        """
        从原始数据中提取需要的数据
        """
        return getProjectInfo(rowData['detail'], rowData['pro'], rowData['progress'])
    

    # private method
    @retry(tries=10)
    def __getJsInfo(self, url):
        """
        获取腾讯公益js中存储的信息
        返回str
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        response = requests.get(url, headers=headers)
        info = re.search(r'\(([\s\S]*)\)', response.text)
        text = info.group(1)
        # 处理文本中存在的双引号以及反斜杠，对其进行转义
        text = text.replace('%5C', '%5C%5C').replace('%22', '%5C%22')
        text = urllib.parse.unquote(text, encoding='utf-8')

        return json.loads(text, strict=False)
