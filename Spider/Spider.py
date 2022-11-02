from abc import ABCMeta, abstractmethod
import json
import time
import requests
import pymongo


class Spider(metaclass=ABCMeta):
    """
    Spider抽象类,所有平台的爬虫均继承于此类
    子类需要实现三个抽象方法
    """

    def __init__(self, collection=None) -> None:
        self.collection = collection

    # public method
    def scrapeOneProjectData(self, projectID) -> None:
        """
        获取并存储一个项目的数据
        """
        if self._isExist(projectID) == False:
            try:
                rowData = self._getRowData(projectID)
                data = self._extractData(rowData)
                self._saveData(data)
            except Exception as e:
                self._errorLog("get project {} failed : {}".format(
                    str(projectID), str(e)))
            else:
                self._successLog(
                    "get project {} succeed".format(str(projectID)))

    def scrapeOnePageData(self, pageNum) -> None:
        """
        抓取并存储一个列表页的数据
        """
        idList = []
        try:
            idList = self._getProjectID(pageNum)
        except Exception as e:
            self._errorLog(
                "get page {} project list failed : {}".format(str(pageNum), str(e)))
        else:
            for projectID in idList:
                self.scrapeOneProjectData(projectID)

    def scrapeAllProjectDataByPage(self, startPage, endPage) -> None:
        """
        以页为单位抓取并存储所有项目数据
        """
        for page in range(startPage, endPage+1):
            self.scrapeOnePageData(page)

    def scrapeAllProjectDataByID(self, startID, endID) -> None:
        """
        以项目为单位抓取并存储所有项目数据
        """
        for projectID in range(startID, endID + 1):
            self.scrapeOneProjectData(projectID)

    # protected method
    @abstractmethod
    def _getProjectID(self, pageNum=None) -> list:
        """
        从项目列表页面获取项目id
        """
        pass

    @abstractmethod
    def _getRowData(self, projectID) -> dict:
        """
        获取原始数据
        """
        pass

    @abstractmethod
    def _extractData(self, rowData) -> dict:
        """
        从原始数据中提取需要的数据
        """
        pass

    def _saveData(self, data) -> None:
        """
        存储提取到的数据
        """
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        """
        判断项目是否已被抓取
        """
        query = self.collection.find_one({"projectID": projectID})
        return query != None

    def _errorLog(self, msg) -> None:
        """
        记录抓取过程中出现的错误
        """
        errorLogFile = "{}_ErrorLog.log".format(self.__class__.__name__)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = "{} [ERROR] {} : {}\n".format(
            formatTime, self.__class__.__name__, msg)
        self._writeToFile(errorLogFile, output)

    def _successLog(self, msg, fileName='SuccessLog') -> None:
        """
        记录抓取过程中出现的成功记录
        """
        successLogFile = "{}_{}.log".format(self.__class__.__name__, fileName)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = "{} [SUCCESS] {} : {}\n".format(
            formatTime, self.__class__.__name__, msg)
        self._writeToFile(successLogFile, output)

    def _writeToFile(self, filePath, msg) -> None:
        """
        写入信息到文件
        """
        with open(filePath, 'a') as file:
            file.write(msg)

    # utils method
    def _getJSONData(self, url, header=None) -> dict:
        """
        发送请求并处理返回的json
        """
        return json.loads(requests.get(url, headers=header).text, strict=False)

    def _postJSONData(self, url, data, header=None) -> dict:
        """
        发送请求并处理返回的json
        """
        return json.loads(requests.post(url, data, headers=header).text, strict=False)
