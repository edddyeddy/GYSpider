from Spider.Spider import *
from bs4 import BeautifulSoup
from ShandongGovSpider.ShanDongGovExtractor import *


class ShanDongGovRegulationSpider(Spider):
    """
    抓取山东省人民政府规章文件数据
    """
    
    
    headers = {
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'zh_choose_410=s; arialoadData=true; ariawapChangeViewPort=false; zh_choose_undefined=s; wondersLog_sdywtb_sdk=%7B%22persistedTime%22%3A1719038134746%2C%22updatedTime%22%3A1719039185396%2C%22sessionStartTime%22%3A1719038134964%2C%22sessionReferrer%22%3A%22%22%2C%22deviceId%22%3A%221a94977233a1be2e6d7af60801868272-6035%22%2C%22LASTEVENT%22%3A%7B%22eventId%22%3A%22wondersLog_pv%22%2C%22time%22%3A1719039185396%7D%2C%22sessionUuid%22%3A4284652083594145%2C%22costTime%22%3A%7B%22wondersLog_unload%22%3A1719039185396%7D%7D',
        'DNT': '1',
        'Origin': 'http://www.shandong.gov.cn',
        'Referer': 'http://www.shandong.gov.cn/col/col235487/index.html?uid=509505&pageNum=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    data = {
        'col': '1',
        'webid': '410',
        'path': 'http://www.shandong.gov.cn/',
        'columnid': '266672',
        'sourceContentType': '3',
        'unitid': '509505',
        'webname': '%E5%B1%B1%E4%B8%9C%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C',
        'permissiontype': '0',
    }


    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        result = set()
        endRecord = 179 # 规章文件数量
        for end in range(15, endRecord, 15):
            url = 'http://www.shandong.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15&unitid=509505&webid=410&path=http://www.shandong.gov.cn/&webname=%E5%B1%B1%E4%B8%9C%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&col=1&columnid=266672&sourceContentType=3&permissiontype=0'.format(
                1 if end - 15 <= 0 else end - 15, end)
            data = requests.post(url, headers= self.headers, data = self.data)
            soup = BeautifulSoup(data.text, 'lxml')
            for item in soup.find_all(attrs={"target": "_blank"}):
                result.add(item.get('href'))

        return list(result)

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowPage = requests.get(url, headers= self.headers)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'url': projectID,
            'rowPage': rowPage.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = ShandongGovExtractor()
        return extractor.extractShandongGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
