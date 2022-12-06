from Spider.Spider import *
from SDCSpider.SDCExtractor import *
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
        extractor = SDCExtractor(
            rowData['base'], rowData['verify'], rowData['caseLabels'], rowData['withdraw'],rowData['userCaseInfo'])
        return extractor.getProjectInfo()

    def _getRowData(self, projectID) -> dict:
        fundingInfo = 'https://api.shuidichou.com/api/cf/v4/get-funding-info'
        verifyInfo = 'https://api.shuidichou.com/api/cf/v4/verification/queryCountVerifyUser'
        caseLabels = 'https://api.shuidichou.com/api/cf/label/get-case-labels'
        withdrawInfo = 'https://api.shuidichou.com/api/cf/v4/drawcash/get-apply-draw/public-message-v2'
        userCaseInfo = 'https://api.shuidichou.com/api/cf/v4/user/get-user-case-info'

        payload = {
            'infoUuid': projectID
        }

        ret = {
            "base": self._postJSONData(fundingInfo, payload, header=self.header),
            "verify": self._postJSONData(verifyInfo,  payload, header=self.header),
            "caseLabels": self._postJSONData(caseLabels, payload, header=self.header),
            "withdraw": self._postJSONData(withdrawInfo, payload, header=self.header),
            "userCaseInfo":self._postJSONData(userCaseInfo, payload, header=self.header),
        }

        return ret

    # default periodic : 10 min
    def saveProjectIDPeriodically(self, periodic=600) -> None:
        return super()._saveProjectIDPeriodically(periodic)

    # default periodic : 1h
    def updateProjectDataPeriodically(self, periodic=3600) -> None:

        def isFinish(rowData):
            return rowData['base']['data']['hasFinished'] == True

        return super()._updateProjectDataPeriodically(isFinish, periodic)

    # default periodic : 12h
    def extractProjectDataPeriodically(self, periodic=43200) -> None:
        super()._extractProjectDataPeriodically(periodic)
        return
