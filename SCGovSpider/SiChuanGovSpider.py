from Spider.Spider import *
import requests
from SCGovSpider.SiChuanGovExtractor import *
from bs4 import BeautifulSoup
import urllib
from retry import retry
from urllib.parse import urljoin
import time
import re


class SichuanGovSpider(Spider):
    """
    抓取四川人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
        }

    # @retry(tries=10, delay=1)
    # def _getProjectID(self, pageNum=None) -> list:
    #     results = set()
    #     pageIndex = "_{}".format(pageNum) if pageNum != 1 else ""
    #     url = f'https://www.sc.gov.cn/10462/c108923/zfgz_list{pageIndex}.shtml' # 规章
    #     print(url)
    #     resp = requests.get(url, headers=self._headers)
    #     resp.encoding = 'utf-8'

    #     soup = BeautifulSoup(resp.text, 'lxml')
    #     # # 规章
    #     list_item = soup.find(attrs={'class':'yxgzul'})
    #     for item in list_item.find_all(attrs={"target": "_blank"}, href=lambda href: href and href.endswith('.shtml')):
    #         complete_link = urllib.parse.urljoin(url, item['href'])
    #         results.add(complete_link)

    #     return results

    # 政府文件
    def _getProjectID(self, pageNum=None) -> list:
        results = list()
        url = 'https://www.sc.gov.cn/cms-scsrmzf/qryZFWJListByConditionsNew'

        payload = {
            'pageSize': 15,
            'pageNum': str(pageNum),
            'channelId': [
                # '973183bdfdc94e9c9060f0707db6dd47',  # 川府发
                # '1c1f2e52f0924af487b00f7d3cfd119d', # 川府规
                # '8ed1f7ae4cca4e1abfd6758159e90b20', # 川府函
                # '7545541b27b543e388b4e84ce37017e6', # 川办发
                # '4634deaa87db498da12f5ca4711f79ea', # 川办规
                'c5207228662c48bda726727268f6356e' # 川办函

            ],
        }

        # 规章
        resp = json.loads(requests.post(url, json=payload,
                          headers=self._headers).text, strict=False)
        for item in resp['results']:
            results.append({
                'projectID': urljoin(url, item['url']),
                'rowData': item['publishedTime']
            })

        return results

    # @retry(tries=10, delay=1)
    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        print(rowData)
        rowPage = requests.get(url)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text,
            'pubDate': rowData
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = SichuanGovExtractor()
        return extractor.extractSichuanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
