from Spider.Spider import *
import requests
from LNGovSpider.LiaoNingGovExtractor import *
import re
from urllib.parse import urljoin


class LiaoningGovSpider(Spider):
    """
    抓取辽宁省人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        base_url = 'https://www.ln.gov.cn/'
        url = 'https://www.ln.gov.cn/web/zwgkx/zfwj/szfl/661e4dc5-{}.shtml'.format(pageNum) # 省政府令
        # url = 'https://www.ln.gov.cn/web/zwgkx/zfwj/szfwj/index.shtml' # 辽政发
        # url = 'https://www.ln.gov.cn/web/zwgkx/zfwj/szfbgtwj/index.shtml' # 辽政办发
        # url = 'https://www.ln.gov.cn/web/zwgkx/zfwj/lzb/56a176e0-{}.shtml'.format(pageNum) # 辽政办
        # url = 'https://www.ln.gov.cn/web/zwgkx/zfwj/bmwj/f1e5925d-{}.shtml'.format(pageNum) # 部门文件
        
        result = list()
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'
        soup = BeautifulSoup(rowData.text, 'lxml')
        items = soup.find_all(attrs={"id": "TITLETEXT"})

        for item in items:
            link = item['href']
            result.append(urljoin(base_url, link))
        return result

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
        extractor = LiaoningGovExtractor()
        return extractor.extractLiaoningGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
