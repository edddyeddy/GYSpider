from Spider.Spider import *
from HenanGovSpider.henanGovSpider import *
from HenanGovSpider.henanGovExtractor import *

class henanGovSpider(Spider):
    """
    抓取河南省人民政府数据
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def __init__(self, col) -> None:
        self.collection = col
        self.CHANNEL_GOV_ORDER = 45000000010115416542055691
        self.CHANNEL_PARTICIPATE = 45000000010115416542079063
        self.CHANNEL_PARTICIPATE_OFFICE = 45000000010115416542055799
        self.CHANNEL_GOV_OTHER = '45000000010115570443879507%2C45000000010116564904834299'
        

    def _getProjectID(self, pageNum) -> list:
        return None
    
    def _getHenanGovFileList(self, pageNum, channel):
        result = list()
        url = 'https://searchapi.henan.gov.cn/open/api/external?keywords=&siteId=4500000001&searchRange=-1000&sortType=200&pageNumber={}&pageSize=15&fileType=3&channelMarkId={}'.format(pageNum, channel)
        rowData = self._getJSONData(url,header=self.header)
        
        for data in rowData['data']['datas']:
            item = {
                'projectID':data['selfUrl'],
                'rowData':data,
            }
            result.append(item)
        return result
        
    def _getRowData(self, projectID, rowData = None) -> dict:
        url = projectID
        rowData = {
            'url': projectID,
            'rowPage': rowData
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = henanGovExtractor()
        return extractor.extractHenanGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID['projectID']}) != None
