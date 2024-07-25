from Spider.Spider import *
import requests
from JXGovSpider.JiangxiGovExtractor import *
from bs4 import BeautifulSoup
import time
import re


class JiangxiGovSpider(Spider):
    """
    抓取江西人民政府数据
    """
    def __init__(self, collection) -> None:
        self.collection = collection

        self.headers = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=9AA825ACE32A16A694A225C371362F24; arialoadData=false; zh_choose_3=s; ariavoiceEnable=false; ariawapChangeViewPort=true; ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false',
            'DNT': '1',
            'Origin': 'https://www.jiangxi.gov.cn',
            'Referer': 'https://www.jiangxi.gov.cn/col/col72576/index.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }   

    # @retry(tries=10, delay=1)
    # def _getProjectID(self, pageNum=None) -> list:
    #     data = {
    #         'col': '1',
    #         'webid': '3',
    #         'path': 'http://www.jiangxi.gov.cn/',
    #         # # 规章
    #         # 'columnid': '71157',
    #         # 'unitid': '464148',
    #         # 'sourceContentType': '3',
    #         # # 省政府
    #         # 'columnid': '72576',
    #         # 'unitid': '464706',
    #         # 'sourceContentType': '1',
    #         # 省政府办公厅
    #         'columnid': '72577',
    #         'unitid': '464706',
    #         'sourceContentType': '1',
            
    #         'webname': '江西省人民政府',
    #         'permissiontype': '0',
    #     }
    #     perpage = 15
    #     result = set()
    #     url = 'https://www.jiangxi.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage={}'.format((pageNum - 1) * perpage, pageNum * perpage, perpage)
    #     print(url)
    #     response = requests.post(url, data, verify=False, headers=self.headers)
    #     response.encoding = 'utf-8'
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     for item in soup.find_all(attrs={"target": "_blank"}, href=lambda x: x and x.endswith('html')):
    #         result.add(item.get('href'))

    #     return result

    # 赣府厅发：https://www.jiangxi.gov.cn/col/col51536/index.html
    @retry(tries=10, delay=1)
    def _getProjectID(self, pageNum=None) -> list:
        url = f'https://www.jiangxi.gov.cn/module/xxgk/serviceinfo.jsp?standardXxgk=0&sortfield=compaltedate:0&fbtime=&texttype=0&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={pageNum}&binlay=&c_issuetime='
        print(url)
        result = set()
        response = requests.post(url, headers=self.headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        for item in soup.find_all(attrs={"target": "_blank"}, href=True):
            result.add(item.get('href'))

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
        extractor = JiangxiGovExtractor()
        return extractor.extractJiangxiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
