from Spider.Spider import *
import requests
from HNGovSpider.HainanGovExtractor import *
from bs4 import BeautifulSoup
import urllib
import time
import re


class HainanGovSpider(Spider):
    """
    抓取海南人民政府数据
    """
    def __init__(self, collection) -> None:
        self.collection = collection
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

    def _getProjectID(self, pageNum=None) -> list:
        results = set()
        pageIndex = "_{}".format(pageNum) if pageNum != 1 else ""
        # url = f'https://www.hainan.gov.cn/hainan/xxyxzfgz/zfgzk{pageIndex}.shtml' # 规章
        url = f'https://www.hainan.gov.cn/hainan/flfgxzgfxwj/fgsjk_ywh{pageIndex}.shtml' # 行政规范性文件
        print(url)
        resp = requests.get(url, headers=self._headers)
        resp.encoding = 'utf-8'

        soup = BeautifulSoup(resp.text, 'lxml')
        # 规章
        # list_item = soup.find(attrs={'class':'gzk1102-nr-m-lm2-r-m'})
        # 行政规范性文件
        list_item = soup.find(attrs={'class':'lm4'})
        for item in list_item.find_all(attrs={"target": "_blank"}, title=True):
            complete_link = urllib.parse.urljoin(url, item['href'])
            results.add(complete_link)

        return results

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
        extractor = HainanGovExtractor()
        return extractor.extractHainanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
