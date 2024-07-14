from Spider.Spider import *
import requests
from NMGGovSpider.NeiMengGuGovExtractor import *
import re
from urllib.parse import urljoin


class NeimengguGovSpider(Spider):
    """
    抓取内蒙古人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/gz/zzqrmzfgz/index{}.html'.format(pageIndex) # 规章
        # url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/xzgfxwj/index{}.html'.format(pageIndex) # 行政规范性文件
        # url = 'https://www.nmg.gov.cn/nmsearch/openSearch/gfxwjkList?sort=time&validity=%E6%9C%89%E6%95%88&publisher=%E8%87%AA%E6%B2%BB%E5%8C%BA%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C%E5%8A%9E%E5%85%AC%E5%8E%85&postCity=nmg&pageNum={}&pageSize=10'.format(pageNum) # 现行行政规范政府
        # url = 'https://www.nmg.gov.cn/nmsearch/openSearch/gfxwjkList?sort=time&validity=%E6%9C%89%E6%95%88&publisher=%E8%87%AA%E6%B2%BB%E5%8C%BA%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&postCity=nmg&pageNum={}&pageSize=10'.format(pageNum) # 现行行政规范政府办
        # url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zc/qtwj/index{}.html'.format(pageIndex) # 其他文件
        url = 'https://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/zzqzfjbgtwj/index{}.html'.format(pageIndex) # 政府文件  
        
        result = set()
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'

        soup = BeautifulSoup(rowData.text, 'lxml')
        items = soup.find_all('a', href=lambda href: href and href.endswith('.html'), target="_blank")
        if len(items) != 0:
            for item in items:
                result.add(urljoin(url, item['href']))
        else:
            resp = json.loads(rowData.text)
            for item in resp['data']['data']:
                result.add(item['docPubUrl'])
        return list(result)

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
        extractor = NeimengguGovExtractor()
        return extractor.extractNeimengguGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
