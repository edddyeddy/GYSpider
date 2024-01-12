from Spider.Spider import *
from ShandongGovSpider.ShanDongGovExtractor import *

class ShandongGovSpider(Spider):
    """
    抓取山东省人民政府数据
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum = None) -> list:
        result = list()
        url = "http://www.shandong.gov.cn/jpaas-jpolicy-console-server/interface/getPolicyByOrgId?title=&year=&category=1&orgId=&validity=&pageNo={}&pageSize=20&sortKey=publish_date".format(pageNum)
        pageUrl = "http://www.shandong.gov.cn/jpaas-jpolicy-web-server/front/info/detail?iid={}"
        rowData = self._getJSONData(url, header=self.header)
        for item in rowData['data']['list']:
            data = {
                'projectID' : pageUrl.format(item['iid']),
                'rowData' : {
                    'publishDate': item['publishDate'],
                    'title': item['title']
                }
            }
            result.append(data)

        return result

    def _getRowData(self, projectID, rowData = None) -> dict:
        rowData = {
            'url' : projectID,
            'rowPage' : requests.get(projectID, headers=self.header).text,
            'rowInfo' : rowData
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = ShandongGovExtractor()
        return extractor.extractShandongGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
