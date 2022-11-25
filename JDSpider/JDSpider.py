from Spider.Spider import *

class JDSpider(Spider):
    '''
    京东公益爬虫
    '''

    def _getProjectID(self, pageNum=None) -> list:
        ids = list()

        url = 'https://gy-api.jd.com/projectList/get?page={}'.format(pageNum)
        rowData = self._getJSONData(url)
        projectList = rowData['data']['data']

        for project in projectList:
            ids.append(project['actId'])

        return ids

    def _getRowData(self, projectID) -> dict:
        basicUrl = 'https://gy-api.jd.com/one/act/detail1?id={}'.format(projectID)
        descUrl = 'https://gy-api.jd.com/project/detail2?id={}'.format(projectID)
        feedBackUrl = 'https://gy-api.jd.com/project/detail3?id={}'.format(projectID)
        messageUrl = 'https://gy-api.jd.com/message/get?page=1&id={}'.format(projectID)
        
        rowData = {
            'projectID' : projectID,
            'basicInfo': self._getJSONData(basicUrl),
            'descInfo': self._getJSONData(descUrl),
            'feedBackInfo': self._getJSONData(feedBackUrl),
            'messageInfo' : self._getJSONData(messageUrl),
        }
        
        return rowData

    def _extractData(self, rowData) -> dict:
        
        data = {
            'projectID' : rowData['projectID'],
            'rowData' : rowData
        }
        
        return data
