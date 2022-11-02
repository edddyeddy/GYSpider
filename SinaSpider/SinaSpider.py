from SinaSpider.SinaExtractor import SinaExtractor
from Spider.Spider import *
from bs4 import BeautifulSoup
import requests
import re


class SinaSpider(Spider):
    """
    新浪微公益爬虫
    """

    def _getProjectID(self, pageNum) -> list:
        """
        从项目列表页面获取项目id
        """
        idList = []
        url = 'https://gongyi.weibo.com/list/personal?on_state=3&page={}'.format(
            str(pageNum))

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.find_all(class_='view_info')
        for info in infos:
            id = re.search(r'-?[1-9]\d*', info.a['href']).group()
            idList.append(int(id))

        return idList

    def _getRowData(self, projectID) -> dict:
        """
        获取原始数据
        """
        rowData = {
            "projectID":None,
            'rowPage': None
        }

        url = "https://gongyi.weibo.com/{}".format(projectID)
        response = requests.get(url)
        rowData['projectID'] = projectID
        rowData['rowPage'] = response.text

        return rowData

    def _extractData(self, rowData) -> dict:
        """
        从原始数据中提取需要的数据
        """
        pass


    def _getWeiboRowData(self, userName) -> dict:
        """
        获取微博用户信息原始数据
        """

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'cookie': 'SINAGLOBAL=5494013191759.565.1619953816904; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFW3f1YrAJiHvXAg0iCbHkU; SUB=_2AkMWTug5f8NxqwJRmPAWzmjrZYlzyQ7EieKgEhniJRMxHRl-yT9jqmAdtRB6Pc7G1xP-U_tm70inuIYk1Fy-j95YelWW; UOR=www.google.com,s.weibo.com,www.google.com.hk; _s_tentry=www.google.com.hk; Apache=9826971605719.627.1648361044537; ULV=1648361044673:40:12:1:9826971605719.627.1648361044537:1648135365883; XSRF-TOKEN=ZB8Yu2WrnpBTRdor6yyu-Zr8; WBPSESS=durPiJxsbzq5XDaI2wW0N3uAnEqIEMjeYl5UkQRmco07SWUnotmtb-h_U-c1sG1g9U-sfJ5g6UM6MCxWTbMo2mel8s4jQG-dkVYDRGwQyA2EhVJ7fZEwe0Mnw6aYd1hQ8xnc-GRWNCQ-K_vv0mwirsuqThGSYB256cmP_3jf2EU='
        }

        url = "https://weibo.com/ajax/profile/info?custom={}".format(userName)
        rowData = self._getJSONData(url, header)

        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = SinaExtractor()
        data = extractor.getProjectInfo(rowData['projectID'],rowData['rowPage'])
        return data

    def extractSinaData(self,projectID) -> dict:
        """
        提取新浪公益数据
        """
        rowData = self.collection.find_one({'projectID':projectID})
        extractor = SinaExtractor()
        data = extractor.getProjectInfo(projectID,rowData['rowPage'])
        return data