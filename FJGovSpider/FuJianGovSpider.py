from Spider.Spider import *
from FJGovSpider.FuJianGovExtractor import*

class FuJianGovSpider(Spider):
    """
    抓取福建省人民政府数据
    """
    
    def __init__(self, collection) -> None:
        self.collection = collection
        
    def _getProjectID(self, pageNum = None) -> list:
        return None

    def _getRowData(self, projectID, rowData = None) -> dict:
        return None

    def _extractData(self, rowData) -> dict:
        extractor = FujianGovExtractor()
        return extractor.extractFujianGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
