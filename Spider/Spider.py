from abc import ABCMeta, abstractmethod
import json
import time
import requests
from retry import retry


class Spider(metaclass=ABCMeta):
    """
    Spider抽象类,所有平台的爬虫均继承于此类
    子类需要实现三个抽象方法
    """

    def __init__(self, collection=None) -> None:
        self.collection = collection

    # public method
    @retry(tries=10, delay=1)
    def scrapeOneProjectData(self, projectID, rowData = None) -> None:
        """
        获取并存储一个项目的数据
        """
        if self._isExist(projectID) == False:
            try:
                rowData = self._getRowData(projectID, rowData)
                data = self._extractData(rowData)
                insertData = {
                    'projectID':projectID,
                }
                
                if rowData is not None:
                    insertData['rowData'] = rowData
                if data is not None:
                    insertData['data'] = data
                    
                self._saveData(insertData)
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
                if isinstance(projectID,dict):
                    self.scrapeOneProjectData(projectID['projectID'], projectID['rowData'])
                else:
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
            if not self._isExist(projectID):
                self.scrapeOneProjectData(projectID)

    # protected method
    @abstractmethod
    def _getProjectID(self, pageNum=None) -> list:
        """
        从项目列表页面获取项目id
        """
        pass

    @abstractmethod
    def _getRowData(self, projectID, rowData = None) -> dict: #部分网站可直接在页面获取所有rowData
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

    def _updateProjectDataPeriodically(self, isFinishFunc, periodic) -> None:
        while True:
            self._successLog('start update project', 'Update')

            cnt = 0
            cursor = self.collection.find({'rowData': {'$exists': False}}, no_cursor_timeout=True, batch_size = 5)
            for item in cursor:
                projectID = item['projectID']
                rowData = None

                # get row data from website
                try:
                    rowData = self._getRowData(projectID)
                except Exception as e:
                    self._errorLog("{},{}".format(__name__, str(e)))
                    continue

                # check and update project data
                if isFinishFunc(rowData):
                    query = {'projectID': projectID}
                    data = {"$set": {"rowData": rowData}}
                    self.collection.update_one(query, data)
                    self._successLog(
                        'update project : {}'.format(projectID), 'Update')
                    cnt += 1


                time.sleep(1)  # 间隔一秒再获取项目数据

            self._successLog("update {} project".format(cnt), 'Update')
            cursor.close()
            time.sleep(periodic)

    def _saveProjectIDPeriodically(self, periodic) -> None:
        while True:
            uuid = None
            self._successLog('start save project id')

            # download uuid list
            try:
                uuid = self._getProjectID()
            except Exception as e:
                self._errorLog("{},{}".format(__name__, str(e)))
                time.sleep(periodic)
                continue
            self._successLog("download {} id".format(len(uuid)))

            # check and save uuid
            cnt = 0
            for id in uuid:
                if not self._isExist(id):
                    self._saveData({"projectID": id})
                    self._successLog("get uuid : {}".format(id))
                    cnt += 1

            self._successLog("save {} id".format(cnt))
            time.sleep(periodic)

    def _extractProjectDataPeriodically(self, periodic) -> None:
        while True:
            query = {
                'rowData': {'$exists': True},
                'data': {"$eq": None}
            }

            self._successLog("start extract project", 'Extract')

            cnt = 0
            for item in self.collection.find(query):
                rowData = item.get('rowData')
                projectID = item['projectID']
                try:
                    data = self._extractData(rowData)
                except Exception as e:
                    print(e)
                    self._errorLog("extract project {} failed : {}".format(
                        str(projectID), str(e)))
                    continue
                
                # update
                query = {'projectID': projectID}
                data = {"$set": {"data": data}}
                self.collection.update_one(query, data)

                cnt += 1
                self._successLog(
                    'update project : {}'.format(projectID), 'Extract')

            self._successLog("extract {} project".format(cnt), 'Extract')
            print("finished")
            time.sleep(periodic)

    # utils method
    @retry(tries=10, delay=1)
    def _getJSONData(self, url, header=None, params=None) -> dict:
        """
        发送请求并处理返回的json
        """
        return json.loads(requests.get(url, headers=header, params=params).text, strict=False)

    @retry(tries=10, delay=1)
    def _postJSONData(self, url, data, header=None) -> dict:
        """
        发送请求并处理返回的json
        """
        return json.loads(requests.post(url, data, headers=header).text, strict=False)
