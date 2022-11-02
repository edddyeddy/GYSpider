from Spider.Spider import *
from QSGYSpider.QSGYExtractor import *


class QSGYSpider(Spider):
    """
    轻松公益爬虫
    """

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }

    def _getProjectID(self, pageNum) -> list:
        """
        从项目列表页面获取项目id
        """
        url = "https://partner-gateway.qschou.com/official/pc/project/succeed?page={}".format(
            pageNum)
        projects = self._getJSONData(url, self.header)['data']
        idList = []
        for project in projects:
            projectID = {
                "id": project['raisefund_no'],
                "channel": project['channel']
            }
            idList.append(projectID)

        return idList

    def _getRowData(self, projectID) -> dict:
        """
        获取原始数据
        """
        rowData = {
            "projectID": projectID,
            "info": None,
            "feed": None,
            "extra": None
        }

        baseURL = "https://partner-gateway.qschou.com/{}/project/{}/".format(
            projectID['channel'], str(projectID['id']))

        rowData["info"] = self._getJSONData(baseURL + "info", self.header)
        rowData["feed"] = self._getJSONData(baseURL + "feed", self.header)
        rowData["extra"] = self._getJSONData(baseURL + "extra", self.header)

        return rowData

    def _extractData(self, rowData) -> dict:
        """
        从原始数据中提取需要的数据
        """
        extractor = QSGYExtractor(rowData['projectID'],
                                  rowData['info'], rowData['feed'], rowData['extra'])
        return extractor.getData()

    # # test
    # def _isExist(self, projectID) -> bool:
    #     return False

    # def _writeToFile(self, filePath, msg) -> None:
    #     print(msg)

    # def _saveData(self, data) -> None:
    #     print(data)
