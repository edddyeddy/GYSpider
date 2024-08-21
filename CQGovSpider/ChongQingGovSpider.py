from Spider.Spider import *
import requests
from CQGovSpider.ChongQingGovExtractor import *
from bs4 import BeautifulSoup
import urllib
from retry import retry
from urllib.parse import urljoin
import json
import time
import re


class ChongqingGovSpider(Spider):
    """
    抓取重庆人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
        }

    # 规章
    # # @retry(tries=10, delay=1)
    # def _getProjectID(self, pageNum=None) -> list:
    #     results = list()
    #     url = f'https://sfj.cq.gov.cn/xzwjk/fileLib/data/pageRule1?current={pageNum}&size=15' # 规章
    #     resp = requests.get(url, headers=self._headers)
    #     resp.encoding = 'utf-8'

    #     row_data = json.loads(resp.text)

    #     for item in row_data['data']['records']:
    #         results.append({
    #             'projectID': item['ruleId'],
    #             'rowData': item['publicationDate']
    #         })
    #     print(row_data)

    #     return results

    # # @retry(tries=10, delay=1)
    # def _getRowData(self, projectID, rowData=None) -> dict:
    #     url = f'https://sfj.cq.gov.cn/xzwjk/fileLib/data/detail/{projectID}'
    #     rowPage = requests.get(url)
    #     rowPage.encoding = 'utf-8'
    #     rowData = {
    #         'projectID': f'https://sfj.cq.gov.cn/xzwjk/page/shizhengfu/guizhangku/detail.html?id={projectID}',
    #         'rowPage': json.loads(rowPage.text),
    #         'pubDate': rowData
    #     }
    #     return rowData


    # @retry(tries=10, delay=1)
    def _getProjectID(self, pageNum=None) -> list:
        results = set()

        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # url = f'https://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/xzgfxwj/szf/index{pageIndex}.html' # 渝府发
        # url = f'https://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/fzhsxgz/fzhsxxzgfxwj/index{pageIndex}.html' # 废止渝府发
        # url = f'https://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/xzgfxwj/szfbgt/index{pageIndex}.html' # 渝府办发
        url = f'https://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/qtgw/index{pageIndex}.html' # 其他文件

        print(url)
        resp = requests.get(url)
        resp.encoding = 'utf-8'

        soup = BeautifulSoup(resp.text, 'lxml')
        # list_item = soup.find(attrs={'class':'zcwjk-list'})
        list_item = soup.find(attrs={'class':'clearfix'}) # 其他文件
        for item in list_item.find_all(attrs={"target": "_blank"}, href=lambda href: href and href.endswith('.html')):
            complete_link = urllib.parse.urljoin(url, item['href'])
            results.add(complete_link)

        return results
    

    # @retry(tries=10, delay=1)
    def _getRowData(self, projectID, rowData=None) -> dict:
        rowPage = requests.get(projectID)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text,
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = ChongqingGovExtractor()
        return extractor.extractChongqingGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
