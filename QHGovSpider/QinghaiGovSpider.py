from Spider.Spider import *
import requests
from QHGovSpider.QingHaiGovExtractor import *


class QinghaiGovSpider(Spider):
    """
    抓取青海人民政府数据
    """

    def __init__(self, collection) -> None:
        self.collection = collection

    def _getProjectID(self, pageNum=None) -> list:
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        # url = 'http://www.qinghai.gov.cn/xxgk/xxgk/fd/lzyj/gzk/index{}.html'.format(pageIndex) # 规章
        # url = f'http://www.qinghai.gov.cn/xxgk/xxgk/fd/lzyj/gfxwj/szf/index{pageIndex}.html' # 省政府行政规范文件
        # url = f'http://www.qinghai.gov.cn/xxgk/xxgk/fd/lzyj/gfxwj/szfb/index{pageIndex}.html' # 省政府行政规范文件
        # url = f'http://www.qinghai.gov.cn/xxgk/1/4/index{pageIndex}.html' # 青政
        # url = f'http://www.qinghai.gov.cn/xxgk/1/6/index{pageIndex}.html' # 青政办
        url = f'http://www.qinghai.gov.cn/xxgk/1/7/index{pageIndex}.html' # 青政办函
        
        print(url)
        result = set()
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'

        soup = BeautifulSoup(rowData.text, 'lxml')
        # list_box = soup.find(attrs={"class":"list-box"})
        # items = list_box.find_all('a', href=lambda href: href and href.endswith('.html'), attrs={"class":"title-main"})
        # 行政规范文件
        items = soup.find_all('a', href=lambda href: href and href.endswith('.html'), attrs={"target":"_blank"})
        for item in items:
            result.add(item['href'])
                
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
        extractor = QinghaiGovExtractor()
        return extractor.extractQinghaiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
