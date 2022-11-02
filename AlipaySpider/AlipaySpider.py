from Spider.Spider import *
from bs4 import BeautifulSoup
import requests
import re


class AlipaySpider(Spider):
    """
    支付宝公益爬虫
    """

    def _getProjectID(self, pageNum) -> list:
        """
        从项目列表页面获取项目id
        """
        url = "https://love.alipay.com/donate/itemList.htm?page={}".format(
            pageNum)

        idList = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.find_all(class_='donate-item-default-title')
        for info in infos:
            id = re.search(r'-?[1-9]\d*', info.a['href']).group()
            idList.append(id)

        return idList

    def _getRowData(self, projectID) -> dict:
        """
        获取原始数据
        """
        rowData = {
            "detail": None,
            "feedBack": None
        }

        detailURL = "https://love.alipay.com/donate/itemDetail.htm?name={}".format(
            str(projectID))

        rowData['detail'] = requests.get(detailURL).text
        rowData['feedBack'] = self.__getFeedBackData(projectID)

        print(rowData)
        return rowData

    def _extractData(self, rowData) -> dict:
        """
        从原始数据中提取需要的数据
        """
        pass

    # private method
    def __getFeedBackData(self, projectID) -> list:
        """
        获取支付宝公益反馈信息原始数据
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'referer': "https://love.alipay.com/donate/itemDetail.htm?name={}".format(projectID)
        }

        feedBackList = []
        pageNum = 1

        while True:
            url = "https://love.alipay.com/donate/showFeedBack.json?name={}&page={}".format(
                str(projectID), str(pageNum))
            feed = self._getJSONData(url, header=header)

            if feed['stat'] != 'ok':
                break

            feedBackList.extend(feed['donateFeedbackPageModelList'])
            pageNum += 1

        return feedBackList