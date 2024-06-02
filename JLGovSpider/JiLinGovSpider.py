from Spider.Spider import *
import requests
from JLGovSpider.JiLinGovExtractor import *
import re
from urllib.parse import urljoin


class JilinGovSpider(Spider):
    """
    抓取吉林省人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        type = 'regulations'
        type = 'normative'
        result = list()

        if type == 'regulations':  # 规章
            url = 'https://was.jl.gov.cn/was5/web/gov/szfgz/response_szf_guizhang.jsp?type=guizhang&callback=result&pageIndex={}&pageSize=10&keyWord=&keyWordType=all'.format(
                pageNum)
            retData = requests.get(url).text
            match = re.search(r'result\((.*)\)', retData)
            json_str = match.group(1)
            rowData = json.loads(json_str)
            for item in rowData['data']:
                result.append(
                    {'rowData': item['RELEASEDATE'], 'projectID': item['docpuburl']})
        elif type == 'normative':  # 行政规范性文件
            url = 'https://infogate.jl.gov.cn/govsearch/jsonp/gkml_xzgf20221026.jsp?callback=result&page={}&size=15&keyword=&keywordCategory=title'.format(
                pageNum)
            retData = requests.get(url).text
            match = re.search(r'result\((.*)\)', retData)
            json_str = match.group(1)
            rowData = json.loads(json_str)
            for item in rowData['list']:
                result.append(
                    {'rowData': item['pubdate'], 'projectID': item['puburl']})


        return result

    def _getRowData(self, projectID, rowData=None) -> dict:
        rowPage = requests.get(projectID)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text,
            'pubData': rowData
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = JilinGovExtractor()
        return extractor.extractJilinGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
