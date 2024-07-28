from Spider.Spider import *
import requests
from HuNanGovSpider.HunanGovExtractor import *
from bs4 import BeautifulSoup
import urllib
from retry import retry
import time
import re


class HunanGovSpider(Spider):
    """
    抓取湖南人民政府数据
    """
    def __init__(self, collection) -> None:
        self.collection = collection
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        
    # @retry(tries=10, delay=1)
    def _getProjectID(self, pageNum=None) -> list:
        results = set()
        pageIndex = "_{}".format(pageNum) if pageNum != 1 else ""
        # url = f'https://www.hunan.gov.cn/hnszf/xxgk/zfgz/index{pageIndex}.html' # 规章
        # url = f'https://www.hunan.gov.cn/hnszf/xxgk/wjk/szfwj/wjk_glrb{pageIndex}.html'  # 省政府文件
        url = f'https://www.hunan.gov.cn/hnszf/xxgk/wjk/szfbgt/wjk_glrb{pageIndex}.html' # 省政府办公厅文件
        print(url)
        resp = requests.get(url, headers=self._headers)
        resp.encoding = 'utf-8'

        soup = BeautifulSoup(resp.text, 'lxml')
        # # 规章
        # list_item = soup.find(attrs={'class':'rules_list'})
        # for item in list_item.find_all(attrs={"target": "_self"}, href=lambda href: href and href.endswith('.html')):
        # 省政府文件
        list_item = soup.find(attrs={'class':'table'})
        for item in list_item.find_all(attrs={"target": "_blank"}, href=lambda href: href and href.endswith('.html')):
            complete_link = urllib.parse.urljoin(url, item['href'])
            results.add(complete_link)

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
        extractor = HunanGovExtractor()
        return extractor.extractHunanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
