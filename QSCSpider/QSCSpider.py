import time
import json

from QSCSpider.QCSExtractor import *
from Spider.Spider import *


class QSCSpider(Spider):
    """
    轻松筹爬虫
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221824031f823132-016de8857dc196-26021a51-2073600-1824031f824304%22%2C%22%24device_id%22%3A%221824031f823132-016de8857dc196-26021a51-2073600-1824031f824304%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D'
    }

    def _getProjectID(self, pageNum=None) -> list:
        """
        从轻松筹主页获取项目ID
        URL:
            1、https://gateway.qschou.com/v3.0.0/index/homepage
            2、https://gateway.qschou.com/v3.0.0/index/order_alert
        """
        homePageUrl = 'https://gateway.qschou.com/v3.0.0/index/homepage'
        orderAlertUrl = 'https://gateway.qschou.com/v3.0.0/index/order_alert'
        uuid = set()

        homePage = self._getJSONData(homePageUrl)
        for project in homePage['data']['project']:
            uuid.add(project['uuid'])

        orderAlert = self._getJSONData(orderAlertUrl)
        for id in orderAlert['data']['project_uuids']:
            uuid.add(id)

        return list(uuid)

    def _extractData(self, rowData) -> dict:
        extractor = QSCExtractor(
            rowData['required'], rowData['extend'], rowData['feed'], rowData['publicity'])
        return extractor.getProjectInfo()

    def _getRowData(self, projectID, rowData = None) -> dict:
        projectUrl = 'https://gateway.qschou.com/v3.0.0/project/index/data'
        feedUrl = 'https://gateway.qschou.com/v3.0.0/feed/index/data'

        ret = {
            "required": self._postJSONData(projectUrl, self.__makePostPayload(projectID, 'required'), header=self.header),
            "extend": self._postJSONData(projectUrl,  self.__makePostPayload(projectID, 'extend'), header=self.header),
            "feed": self._postJSONData(feedUrl, self.__makePostPayload(projectID, 'feed'), header=self.header),
            "publicity": self._postJSONData(feedUrl, self.__makePostPayload(projectID, 'publicity'), header=self.header),
        }

        return ret

    def __makePostPayload(self, uuid, tag):

        payload = {"tag": tag,
                   "uuid": uuid,
                   }
        return json.dumps(payload)

    # default periodic : 1h
    def updateProjectDataPeriodically(self, periodic=3600) -> None:

        def isFinish(rowData):
            return rowData['required']['data']['project']['time_left_numb'] == '0'

        return super()._updateProjectDataPeriodically(isFinish, periodic)

    # default periodic : 10 min
    def saveProjectIDPeriodically(self, periodic=600) -> None:
        super()._saveProjectIDPeriodically(periodic)

    # default periodic : 12h
    def extractProjectDataPeriodically(self, periodic=43200) -> None:
        super()._extractProjectDataPeriodically(periodic)
