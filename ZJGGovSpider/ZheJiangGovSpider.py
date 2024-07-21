from Spider.Spider import *
import requests
from ZJGGovSpider.ZheJiangGovExtractor import *
from bs4 import BeautifulSoup
import re


class ZhejiangGovSpider(Spider):
    """
    抓取浙江人民政府数据
    """
    def __init__(self, collection) -> None:
        self.collection = collection

    # 规章
    def _getProjectID(self, pageNum=None) -> list:
       
        url = 'https://www.zj.gov.cn/module/xxgk/ruleinfo.jsp?fbtime=&texttype=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={}&binlay=&c_issuetime=&isAllList=1&standardXxgk=[object%20HTMLInputElement]'.format(
            pageNum)
        data = {
            'i_style': 1,
            'i_id': 1229604638,
            'standardXxgk': 0
        }

        result = []
        print(url)
        response = requests.post(url, data)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all(attrs={"class": "zc_list_tit"})
        for item in items:
            result.append( item['href'])
        return result
    
    # def _getProjectID(self, pageNum=None) -> list:
    #     data = {
    #         'col': '1',
    #         'appid': '1',
    #         'webid': '3096',
    #         'path': '/',
    #         # # 省政府有效
    #         # 'columnid': '1229017138',
    #         # 'unitid': '7893195',
    #         # # 省政府失效
    #         # 'columnid': '1229621583',
    #         # 'unitid': '7893217',
    #         # 省政府废止
    #         # 'columnid': '1229591319',
    #         # 'unitid': '7893235',
    #         # # 省政府办公厅有效
    #         # 'columnid': '1229017139',
    #         # 'unitid': '7893253',
    #         # # 省政府办公厅失效
    #         # 'columnid': '1229621584',
    #         # 'unitid': '7893271',
    #         # # 省政府办公厅废止
    #         # 'columnid': '1229591320',
    #         # 'unitid': '7893289',
    #         # 省政府其他文件
    #         # 'columnid': '1229019364',
    #         # 'unitid': '7893307',
    #         # 省政府办公厅其他文件
    #         'columnid': '1229019365',
    #         'unitid': '7893325',

    #         'sourceContentType': '3',
    #         'webname': '浙江省人民政府门户网站',
    #         'permissiontype': '0',
    #     }

    #     result = set()
    #     url = 'https://www.zj.gov.cn/module/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=10'.format((pageNum-1)* 10, pageNum *10)
    #     print(url)
    #     response = requests.post(url, data)
    #     response.encoding = 'utf-8'
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     for item in soup.find_all(attrs={"target": "_blank"}):
    #         result.add(item.get('href'))

    #     return result

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
        extractor = ZhejiangGovExtractor()
        return extractor.extractZhejiangGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
