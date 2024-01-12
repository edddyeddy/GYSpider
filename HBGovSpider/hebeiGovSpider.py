from Spider.Spider import *
from HBGovSpider.hebeiGovExtractor import *
from bs4 import BeautifulSoup
import requests

class hebeiGovSpider(Spider):
    """
    抓取河北省人民政府数据
    """

    def __init__(self, dataCol) -> None:
        self.collection = dataCol
        
    def _getProjectIDByType(self, pageNum, url, attrs) -> list:
        fileUrlList = list()
        url = url.format(pageNum)
        baseUrl = 'https://info.hebei.gov.cn'
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'
        soup = BeautifulSoup(rowData.text, "lxml")
        items = soup.find_all(attrs=attrs)
        for item in items:
            href = item.a.get('href')
            fileUrlList.append(baseUrl + href)
        return fileUrlList

    def _getProjectID(self, pageNum) -> list:
        return None

    def _getRowData(self, projectID, rowData=None) -> dict:
        rowData = rowData = requests.get(projectID)
        rowData.encoding = 'utf-8'
        ret = {
            'projectID': projectID,
            'rowPage': rowData.text
        }
        return ret

    def _extractData(self, rowData) -> dict:
        extractor = hebeiGovExtractor()
        return extractor.extractHenanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
