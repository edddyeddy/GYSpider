from Spider.Spider import *
from XiamenGovSpider.xiamenGovExtractor import XiamenGovExtractor

class XiamenGovSpider(Spider):
    """
    抓取厦门市人民政府数据
    """

    def __init__(self, dataCol) -> None:
        self.collection = dataCol

    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.xm.gov.cn/ssp/search/api/apiSearch?siteId=40280d1172da01550172dadfb0640004&apiName=zcwjk&searchFiled=doctitle&chnlIdList=26370%2C5838%2C5839%2C43642%2C43643%2C36348&isChange=1&fullKey=N&sortFiled=-pubdate&page={}&rows=15'.format(
            pageNum)
        fileUrlList = list()

        rowData = self._getJSONData(url)
        datas = rowData['datas']
        for data in datas:
            fileUrlList.append(data['docpuburl'])

        return fileUrlList

    def _getRowData(self, projectID, rowData = None) -> dict:
        url = projectID
        rowData = {
            'url': projectID,
            'rowPage': requests.get(url).text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = XiamenGovExtractor()
        return extractor.extractXiamenGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
