from weiboSpider.weiboExtractor import weiboExtractor
from Spider.Spider import *
import time

class weiboSpider(Spider):
    """
    抓取微博数据
    """

    def __init__(self, rowCol, dataCol) -> None:
        self.rowCol = rowCol
        self.dataCol = dataCol

    def _getProjectID(self, pageNum) -> list:
        weiboID = set()
        for item in self.rowCol.find():
            sponsorID = item['sponsor']['weibo'].split('/')[-1]
            receiverID = item['receiver']['weibo'].split('/')[-1]
            if sponsorID != '':
                weiboID.add(sponsorID)
            if receiverID != '':
                weiboID.add(receiverID)

        return list(weiboID)

    def _getRowData(self, projectID) -> dict:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'cookie': 'SINAGLOBAL=5494013191759.565.1619953816904; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFW3f1YrAJiHvXAg0iCbHkU; SUB=_2AkMWTug5f8NxqwJRmPAWzmjrZYlzyQ7EieKgEhniJRMxHRl-yT9jqmAdtRB6Pc7G1xP-U_tm70inuIYk1Fy-j95YelWW; UOR=www.google.com,s.weibo.com,www.google.com.hk; _s_tentry=www.google.com.hk; Apache=9826971605719.627.1648361044537; ULV=1648361044673:40:12:1:9826971605719.627.1648361044537:1648135365883; XSRF-TOKEN=ZB8Yu2WrnpBTRdor6yyu-Zr8; WBPSESS=durPiJxsbzq5XDaI2wW0N3uAnEqIEMjeYl5UkQRmco07SWUnotmtb-h_U-c1sG1g9U-sfJ5g6UM6MCxWTbMo2mel8s4jQG-dkVYDRGwQyA2EhVJ7fZEwe0Mnw6aYd1hQ8xnc-GRWNCQ-K_vv0mwirsuqThGSYB256cmP_3jf2EU='
        }

        url = "https://weibo.com/ajax/profile/info?custom={}".format(projectID)
        rowData = self._getJSONData(url, header)

        ret = {
            "projectID": projectID,
            "rowData": rowData['data'],
            "getTime": time.time()
        }

        return ret

    def _extractData(self, rowData) -> dict:
        extractor = weiboExtractor()
        return extractor.extractWeiboData(rowData)

    def _saveData(self, data) -> None:
        self.dataCol.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.dataCol.find_one({'projectID': projectID}) != None
