from Spider.Spider import *
import requests
from GZGovSpider.GuiZhouGovExtractor import *
from bs4 import BeautifulSoup
import time
import re


class GuiZhouGovSpider(Spider):
    """
    抓取贵州人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    @retry(tries=10, delay=1)
    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/szfl/index{pageIndex}.html' # 省政府令
        # url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/qff/index{pageIndex}.html' # 黔府发
        # url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/qfh/index{pageIndex}.html' # 黔府函
        # url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/qfbf/index{pageIndex}.html' # 黔府办发
        # url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/qfbh/index{pageIndex}.html' # 黔府办函
        url = f'https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/wjxgfzqk/sxfzwj/index{pageIndex}.html' # 黔府办函
       
        print(url)
        result = set()
        response = requests.get(url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')
        content_soup = soup.find(attrs={"class": "PageMainBox aBox"})
        items = content_soup.find_all(attrs={"target": "_blank"},title=True)
        for item in items:
            result.add(item['href'])
        time.sleep(1)
        return result

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
        extractor = GuiZhouGovExtractor()
        return extractor.extractGuiZhouGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
