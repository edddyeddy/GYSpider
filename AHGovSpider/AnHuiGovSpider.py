from Spider.Spider import *
import requests
from AHGovSpider.AnHuiGovExtractor import *
from bs4 import BeautifulSoup
import time
import re


class AnHuiGovSpider(Spider):
    """
    抓取安徽人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        # # 规章
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.5646464928559716&labelName=publicInfoList&siteId=6781961&pageSize=15&pageIndex={}&action=list&fuzzySearch=&fromCode=title&keyWords=&sortType=&isDate=true&dateFormat=yyyy-MM-dd&length=46&organId=1681&type=6&catIds=6718161&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fxxgk%2Fpublic_gzk'.format(
        #     pageNum)
        # 省政府行政规范有效
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.3173616946003832&labelName=publicInfoList&siteId=6781961&pageSize=15&pageIndex={}&isDate=true&dateFormat=yyyy-MM-dd&length=50&active=0&organId=1681&type=6&fileNum=&filterFileNum=&catIds=6718251&fromCode=title&sortType=&action=list&fuzzySearch=&keyWords=&publicDivId=szf&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahgov%2FpublicInfoList_xzgfk'.format(
        #     pageNum)
        # # 省政府行政规范失效
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.1407225024827341&labelName=publicInfoList&siteId=6781961&pageSize=15&pageIndex={}&isDate=true&dateFormat=yyyy-MM-dd&length=50&active=0&organId=1681&type=6&fileNum=&filterFileNum=&catIds=6718271&fromCode=title&sortType=&action=list&fuzzySearch=&keyWords=&publicDivId=tab_0_1&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahgov%2FpublicInfoList_xzgfk'.format(
        #     pageNum)
        # # 省政府办公厅行政规范有效
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.9146965787516566&labelName=publicInfoList&siteId=6781961&pageSize=15&pageIndex={}&isDate=true&dateFormat=yyyy-MM-dd&length=50&active=0&organId=1681&type=6&fileNum=&filterFileNum=&catIds=6718261&fromCode=title&sortType=&action=list&fuzzySearch=&keyWords=&publicDivId=szfbgt&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahgov%2FpublicInfoList_xzgfk'.format(
        #     pageNum)
        # 省政府办公厅行政规范失效
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.7390693979553284&labelName=publicInfoList&siteId=6781961&pageSize=15&pageIndex={}&isDate=true&dateFormat=yyyy-MM-dd&length=50&active=0&organId=1681&type=6&fileNum=&filterFileNum=&catIds=6718271&fromCode=title&action=list&keyWords=&publicDivId=tab_0_1&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahgov%2FpublicInfoList_xzgfk'.format(
        #     pageNum)
        # 政策法规-省政府文件
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.253923446148433&labelName=publicInfoList&siteId=6781961&pageSize=18&pageIndex={}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=1681&type=4&catId=6708461&catIds=&cId=&keyWords=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahxxgk%2Fxxgk%2FpublicInfoList_new_ah'.format(
        #     pageNum)
        # # 政策法规-省政府办公厅文件
        url = 'https://www.ah.gov.cn/site/label/8888?_=0.973595787490769&labelName=publicInfoList&siteId=6781961&pageSize=18&pageIndex={}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=1681&type=4&catId=6708471&catIds=&cId=&keyWords=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahxxgk%2Fxxgk%2FpublicInfoList_new_ah'.format(
            pageNum)
        # # 政策法规-已废止和失效
        # url = 'https://www.ah.gov.cn/site/label/8888?_=0.23028224657365048&labelName=publicInfoList&siteId=6781961&pageSize=18&pageIndex={}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=1681&type=4&catId=6708481&catIds=&cId=&keyWords=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fahxxgk%2Fxxgk%2FpublicInfoList_new_ah'.format(
        #     pageNum)
       
        print(url)
        result = set()
        response = requests.get(url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')
        # items = soup.find_all(attrs={"target": "_blank", "class": "atit"})
        # # 行政规范
        # items = soup.find_all(attrs={"target": "_blank"}, title=True)
        # 政策法规
        items = soup.find_all(attrs={"target": "_blank", 'class': 'title'})
        for item in items:
            result.add(item['href'])
        time.sleep(1)
        return result

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowPage = requests.get(url)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = AnHuiGovExtractor()
        return extractor.extractAnHuiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
