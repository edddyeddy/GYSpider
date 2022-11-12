from Spider.Spider import *
import time

class SDCSpider(Spider):
    """
    水滴筹爬虫
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Connection': 'close'
    }

    def __init__(self, Authorization, collection=None) -> None:
        super().__init__(collection)
        self.Authorization = Authorization

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
            'AuthorizationV2': self.Authorization
        }

        resp = self._postJSONData(url, postPayload, self.header)
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
            uuid = None

            try:
                uuid = self._getProjectID()
            except Exception as e:
                print("{},{}".format(__name__, str(e)))
                continue

            cnt = 0
            self._successLog("download {} id".format(len(uuid)))
            for id in uuid:
                if not self._isExist(id):
                    self._saveData({"projectID": id})
                    self._successLog("get uuid : {}".format(id))
                    cnt += 1

            self._successLog("get {} id".format(cnt))

            # get id per 30 min
            time.sleep(60 * 30)

    def updateProjectDataPeriodically(self) -> None:
        while True:

            for item in self.collection.find({'rowData': {'$exists': False}}):
                projectID = item['projectID']
                rowData = None
                try:
                    rowData = self._getRowData(projectID)
                except Exception as e:
                    print("{},{}".format(__name__, str(e)))
                    continue

                if rowData['base']['data']['hasFinished'] == True:
                    # update
                    query = {'projectID': projectID}
                    data = {"$set": {"rowData": rowData}}
                    self.collection.update_one(query, data)

                    self._successLog(
                        'update project : {}'.format(projectID), 'Update')

                time.sleep(5)

            # update project pre 12 hour
            time.sleep(60 * 60 * 12)
