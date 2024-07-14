from bs4 import BeautifulSoup
from Spider.Spider import *
import requests
import re
import time
import urllib.parse
from TJGovSpider.TianJinGovExtractor import *


class TianJinGovSpider(Spider):
    """
    抓取天津市人民政府数据
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        result = list()
        page_url = "" if pageNum == 1 else "_{}".format(pageNum - 1)
        base_url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/'
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/index{}.html'.format(page_url)
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/index_10954{}.html'.format(page_url) # 津政令
        url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/index_10960{}.html'.format(page_url) # 津政发
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/index_10873{}.html'.format(page_url) # 津政函
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzfbgt/index_10989{}.html'.format(page_url) # 津政办发
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzfbgt/index_10896.html{}.html'.format(page_url) # 津政办函
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/index_10904{}.html'.format(page_url) # 津政规
        # url = 'https://www.tj.gov.cn/zwgk/szfwj/tjsrmzfbgt/index_10935{}.html'.format(page_url) # 津政办规
        print(url)
        row_data = requests.get(url, headers=self.header)
        row_data.encoding = 'utf-8'
        soup = BeautifulSoup(row_data.text, 'lxml')
        items = soup.find_all('a', href=True, title=True, target="_blank",attrs={"class": "list-item-con"})
        for item in items:
            href = item['href']
            print(href)
            complete_link = urllib.parse.urljoin(base_url, href)
            result.append(complete_link)
        
        return result


    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowPage = requests.get(url, headers=self.header)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = TianJinGovExtractor()
        return extractor.extractTianJinGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None