import time
import json

from Spider.Spider import *
import pymongo


class SDCSpider(Spider):
    """
    水滴筹爬虫
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def _getProjectID(self, pageNum=None) -> list:
        """
        从水滴筹主页获取项目ID
        URL:
            1、https://api.shuidichou.com/api/charity/love-home/find-love-help-case-v2'
        """
        url = 'https://api.shuidichou.com/api/charity/love-home/find-love-help-case-v2'

        uuid = set()

        postPayload = {
            'currentPage': 1,
            'pageSize': 1000,
            'AuthorizationV2': 'laYVYhSx3qQ2iS0H0oBBB3xAMgbScplz6gKhabeDxR0='
        }

        resp = self._postJSONData(url, postPayload)
        projectList = resp['data']['caseInfoVoList']

        for project in projectList:
            uuid.add(project['infoId'])

        return list(uuid)

    def _extractData(self, rowData) -> dict:
        return super()._extractData(rowData)

    def _getRowData(self, projectID) -> dict:
        fundingInfo = 'https://api.shuidichou.com/api/cf/v4/get-funding-info'
        verifyInfo = 'https://api.shuidichou.com/api/cf/v4/verification/queryCountVerifyUser'
        caseLabels = 'https://api.shuidichou.com/api/cf/label/get-case-labels'
        withdrawInfo = 'https://api.shuidichou.com/api/cf/v4/drawcash/get-apply-draw/public-message-v2'

        payload = {
            'infoUuid': projectID
        }

        ret = {
            "base": self._postJSONData(fundingInfo, payload, header=self.header),
            "verify": self._postJSONData(verifyInfo,  payload, header=self.header),
            "caseLabels": self._postJSONData(caseLabels, payload, header=self.header),
            "withdraw": self._postJSONData(withdrawInfo, payload, header=self.header),
        }

        return ret

    def saveProjectIDPeriodically(self) -> None:
        while True:
            uuid = self._getProjectID()
            cnt = 0

            for id in uuid:
                if not self._isExist(id):
                    self._saveData({"projectID": id})
                    self._successLog("get uuid : {}".format(id))
                    cnt += 1

            self._successLog("get {} id".format(cnt))

            # get id per 20 min
            time.sleep(60 * 20)

    def updateProjectDataPeriodically(self) -> None:
        while True:
            for item in self.collection.find({'rowData': {'$exists': False}}):
                projectID = item['projectID']
                rowData = None
                try:
                    rowData = self._getRowData(projectID)
                except Exception as e:
                    print(e)
                    continue

                if rowData['base']['data']['hasFinished'] == True:
                    # update
                    query = {'projectID': projectID}
                    data = {"$set": {"rowData": rowData}}
                    self.collection.update_one(query, data)

                    self._successLog(
                        'update project : {}'.format(projectID), 'Update')

            # update project pre 1 hour
            time.sleep(60 * 60)
