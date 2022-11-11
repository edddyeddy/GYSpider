import time
import json

from QSCSpider.QCSExtractor import *
from Spider.Spider import *
import pymongo


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

        # print(uuid)

        return list(uuid)

    def _extractData(self, rowData) -> dict:
        extractor = QSCExtractor(
            rowData['required'], rowData['extend'], rowData['feed'], rowData['publicity'])
        return extractor.getProjectInfo()

    def _getRowData(self, projectID) -> dict:
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

    def updateProjectData(self) -> None:
        while True:
            for item in self.collection.find({'rowData': {'$exists': False}}):
                projectID = item['projectID']
                rowData = None
                try:
                    rowData = self._getRowData(projectID)
                except Exception as e:
                    print(e)
                    continue

                if rowData['required']['data']['project']['time_left_numb'] == '0':
                    # update
                    query = {'projectID': projectID}
                    data = {"$set": {"rowData": rowData}}
                    self.collection.update_one(query, data)

                    self._successLog(
                        'update project : {}'.format(projectID), 'Update')

            # update project pre 12 hour
            time.sleep(60 * 60 * 12)

    def saveProjectIDPeriodically(self) -> None:
        while True:
            uuid = None 
            try:
                uuid = self._getProjectID()
            except Exception as e:
                print("{},{}".format(__name__,str(e)))
                continue

            cnt = 0
            for id in uuid:
                if not self._isExist(id):
                    self._saveData({"projectID": id})
                    self._successLog("get uuid : {}".format(id))
                    cnt += 1

            self._successLog("get {} id".format(cnt))

            # get id per 5 min
            time.sleep(60 * 5)

    def extractProjectDataPeriodically(self) -> None:
        while True:
            query = {
                'rowData': {'$exists': True},
                'data': {'$exists': False}
            }

            for item in self.collection.find(query):
                rowData = item.get('rowData')
                projectID = item['projectID']
                data = self._extractData(rowData)
                # update
                query = {'projectID': projectID}
                data = {"$set": {"data": data}}
                self.collection.update_one(query, data)

                self._successLog(
                    'update project : {}'.format(projectID), 'Extract')

            # update project pre 1 hour
            time.sleep(60 * 60)
