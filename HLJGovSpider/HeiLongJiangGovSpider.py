from Spider.Spider import *
import requests
from HLJGovSpider.HeiLongJiangGovExtractor import *
from urllib.parse import urljoin


class HeilongjiangGovSpider(Spider):
    """
    抓取黑龙江省人民政府数据
    """

    _headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        results = list()
        # 规章
        # url = 'https://www.hlj.gov.cn/common/search/817052cbb3a94d0d8217824e7a3aca53?page={}&_pageSize=15&_isAgg=true&_isJson=true&_template=index&_rangeTimeGte=&_channelName='.format(
        #     pageNum)
        # 行政规范性文件_省政府
        # url = 'https://www.hlj.gov.cn/common/search/b9e6fb997e274f05a8f8b0f2b7582a1c?page={}&_pageSize=10&_isAgg=true&_isJson=true&_template=index&_rangeTimeGte=&_channelName='.format(pageNum)
        # 行政规范性文件_省政府办公厅
        # url = 'https://www.hlj.gov.cn/common/search/779f8eda2ae847c2a46893fcc05284fc?page={}&_pageSize=10&_isAgg=true&_isJson=true&_template=index&_rangeTimeGte=&_channelName='.format(pageNum)
        # 行政规范性文件_已废止文件
        # url = 'https://www.hlj.gov.cn/common/search/2fd8a707a48a469c9b9c96fea87d675a?_isAgg=false&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page={}'.format(pageNum)
        # 其他文件
        url = 'https://www.hlj.gov.cn/common/search/abb05ecdbbd04a4ca5474735769579dd?page={}&_pageSize=10&_isAgg=true&_isJson=true&_template=index&_rangeTimeGte=&_channelName='.format(pageNum)

        base_url = 'https://www.hlj.gov.cn/'
        row_data = self._getJSONData(url, header=self._headers)
        for item in row_data['data']['results']:
            results.append(urljoin(base_url, item['url']))

        return results

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        row_page = requests.get(url, headers=self._headers)
        row_page.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': row_page.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = HeilongjiangGovExtractor()
        return extractor.extractHeilongjiangGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
