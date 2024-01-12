from bs4 import BeautifulSoup
from Spider.Spider import *
import requests
import re
import time
from JSGovSpider.JiangSuGovExtractor import *


class JiangSuGovSpider(Spider):
    """
    抓取江苏省人民政府数据
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Origin': 'https://www.jiangsu.gov.cn',
        'Referer': 'https://www.jiangsu.gov.cn/col/col84241/index.html?uid=356374&pageNum=1',
    }

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        pageNum = 5045  # 硬编码总项目数
        form_data = {
            'col': '1',
            'appid': '1',
            'webid': '1',
            'path': '/',
            'columnid': '84242',
            'sourceContentType': '3',
            'unitid': '356383',
            'webname': '江苏省人民政府',
            'permissiontype': '0'
        }
        
        result = list()
        
        range_data = list(range(1, pageNum + 1))
        interval_size = 100
        
        intervals = []
        for i in range(0, len(range_data), interval_size):
            begin = i + 1
            end = min(i + interval_size, len(range_data))
            current_interval = [begin, end]
            intervals.append(current_interval)
        
        for begin, end in intervals:
            url = 'https://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage={}'.format(
                begin, end, interval_size)
            rowData = requests.post(url, headers=self.header, data=form_data).text
            pattern = re.compile(r'<record>.*?href="(.*?)".*?</record>', re.DOTALL)
            matches = re.findall(pattern, rowData)
            for match in matches:
                result.append(match)
            # print(result)
            time.sleep(60)
        return result

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowData = {
            'projectID': projectID,
            'rowPage': requests.get(url, headers=self.header).text
        }
        # time.sleep(60)
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = JiangSuGovExtractor()
        return extractor.extractJiangSuGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
    
    def updateProjectDataPeriodically(self, periodic):
        def isFinishFunc(rowData):
            return "如果您是网站管理员，请登录知道创宇云防御" not in rowData['rowPage']
        return self._updateProjectDataPeriodically(isFinishFunc, periodic)
