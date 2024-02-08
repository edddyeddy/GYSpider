from bs4 import BeautifulSoup
from Spider.Spider import *
import requests
import re
import time
import urllib.parse
from BJGovSpider.BeiJingGovExtractor import *


class BeiJingGovSpider(Spider):
    """
    抓取北京市人民政府数据
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'Path=/; __jsluid_s=c438c93da56489fc80ab9d113072c267; arialoadData=false; _va_id=8c0b822130822bae.1706093728.2.1706101635.1706093973.; JSESSIONID=MGI3N2Y4NjUtYjM4ZS00YmMxLWE0ODItMzhjN2FhZTk3ZmVj',
        'DNT': '1',
        'Referer': 'https://www.beijing.gov.cn/zhengce/gfxwj/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


    def __init__(self, collection) -> None:
        self.collection = collection
        
    def __getProjectIDList(self, url) -> list:
        result = list()
        if url is None:
            return result
        row_data = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(row_data.text, 'lxml')
        items = soup.find_all('a', href=True, title=True, target="_blank")
        for item in items:
            href = item['href']
            complete_link = urllib.parse.urljoin(url, href)
            result.append(complete_link)
            
        return result
    
    def _getProjectID(self, pageNum=None) -> list:
        new_project_url = 'https://www.beijing.gov.cn/zhengce/gfxwj/'
        old_project_url = None
        
        return self.__getProjectIDList(new_project_url)


    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowData = {
            'projectID': projectID,
            'rowPage': requests.get(url, headers=self.headers).text
        }
        if '如果您是网站管理员，请登录知道创宇云防御' in rowData['rowPage']:
            print('error')
        time.sleep(1)
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = BeiJingGovExtractor()
        return extractor.extractBeiJingGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
    
    def updateProjectDataPeriodically(self, periodic):
        def isFinishFunc(rowData):
            return "如果您是网站管理员，请登录知道创宇云防御" not in rowData['rowPage']
        return self._updateProjectDataPeriodically(isFinishFunc, periodic)
