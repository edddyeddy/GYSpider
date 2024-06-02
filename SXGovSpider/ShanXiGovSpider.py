from Spider.Spider import *
import requests
from SXGovSpider.ShanXiGovExtractor import *
import re
from urllib.parse import urljoin


class ShanxiGovSpider(Spider):
    """
    抓取山西省人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # 规章
        # url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/zc/gz/sjzfgz/index{}.shtml'.format(
        #     pageIndex)
        # 省政府文件
        # url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/fdzdgknr/lzyj/szfwj/index{}.shtml'.format(
        #     pageIndex)
        # 省政府办公厅文件
        # url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/fdzdgknr/lzyj/szfbgtwj/index{}.shtml'.format(
        #     pageIndex)
        # 废止省政府文件
        url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/zc/xzgfxwj/bmgfxwj1/szfzcbm_76475/srmzf/index_11287{}.shtml'.format(
            pageIndex)
        # 废止省政府办文件
        # url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/zc/xzgfxwj/bmgfxwj1/szfzcbm_76475/srmzfbgt/index_11288{}.shtml'.format(
        #     pageIndex)
        result = list()
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'

        soup = BeautifulSoup(rowData.text, 'lxml')
        items = soup.find_all(
            attrs={"class": "sxinfo-pubfiles-item sxinfo-gzkfiles-item"})
        if len(items) == 0 : 
            items = soup.find_all(
                attrs={"class": "sxinfo-pubfiles-item"})
            
        for item in items:
            link = item.find(
                'a', href=lambda href: href and href.endswith('.shtml'))
            result.append(urljoin(url, link['href']))
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
        extractor = ShanxiGovExtractor()
        return extractor.extractShanxiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
