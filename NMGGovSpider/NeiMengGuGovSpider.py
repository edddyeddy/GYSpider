from Spider.Spider import *
import requests
from NMGGovSpider.NeiMengGuGovExtractor import *
import re
from urllib.parse import urljoin


class NeimengguGovSpider(Spider):
    """
    抓取内蒙古人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/gz/zzqrmzfgz/index{}.html'.format(pageIndex) # 规章
        # url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/xzgfxwj/index{}.html'.format(pageIndex) # 行政规范文件
        url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/qtwj/index{}.html'.format(pageIndex) # 其他文件
        
        result = set()
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'

        soup = BeautifulSoup(rowData.text, 'lxml')
        items = soup.find_all('a', href=lambda href: href and href.endswith('.html'), target="_blank")
        for item in items:
            result.add(urljoin(url, item['href']))
        return list(result)

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
        extractor = NeimengguGovExtractor()
        return extractor.extractNeimengguGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
