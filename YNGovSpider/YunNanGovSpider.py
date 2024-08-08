from Spider.Spider import *
import requests
from YNGovSpider.YunNanGovExtractor import *
from bs4 import BeautifulSoup
import urllib.parse
import time
import re


class YunNanGovSpider(Spider):
    """
    抓取云南人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    # # 行政规范文件/规章
    # @retry(tries=10, delay=1)
    # def _getProjectID(self, pageNum=None) -> list:
    #     url = 'https://api.so-gov.cn/query/s'
    #     data = {
    #         'tabType': '0',
    #         'siteCode': 'ynzcwjk',
    #         # 省政府办公厅行政规范
    #         # 'tab': 'gfxwjk',
    #         # 'SOURCE': '云南省人民政府办公厅',
    #         # 'SOURCE': '云南省人民政府',
    #         # 规章
    #         'tab': 'gz',
    #         'qt': '',
    #         'sort': 'relevance',
    #         'keyPlace': '1',
    #         'timeOption': '0',
    #         'page': str(pageNum),
    #         'pageSize': '20',
    #         'navContent': '1',
    #         'ie': '91d2ff2c-c0d3-46f3-81cb-320389f5e83f',
    #     }
    #     results = list()
    #     resp = self._postJSONData(url, data)
    #     for item in resp['resultDocs']:
    #         results.append(item['data']['url'])

    #     return results
    
    # 政策文件
    @retry(tries=10, delay=1)
    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        url = f'https://www.yn.gov.cn/zwgk/zcwj/zxwj/index{pageIndex}.html'

        results = list()

        rowData = requests.get(url)
        soup = BeautifulSoup(rowData.text, 'lxml')
        tableSoup = soup.find('table')
        links = tableSoup.find_all('a', href=True)

        for item in links:
            complete_link = urllib.parse.urljoin(url, item['href'])
            results.append(complete_link)

        return results

    @retry(tries=10, delay=1)
    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowPage = requests.get(url)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = YunNanGovExtractor()
        return extractor.extractYunNanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
