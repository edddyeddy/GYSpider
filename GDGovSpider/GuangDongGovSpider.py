from Spider.Spider import *
import requests
from GDGovSpider.GuangDongGovExtractor import *
import re

class GuangDongGovSpider(Spider):
    """
    抓取广东省人民政府数据
    """
    
    def __init__(self, collection) -> None:
        self.collection = collection
        
        
    def __getFileUrl(self, listRowData):
        result = list()
        soup = BeautifulSoup(listRowData, 'lxml')
        viewList = soup.find(attrs={"class": "viewList"})
        items = viewList.find_all(attrs={"class": "name"})
        baseUrl = 'http://www.gd.gov.cn/gkmlpt/content/'
        
        for item in items:
            a_tag = item.a
            if a_tag is not None:
                href = a_tag.get('href')
                re_match = re.search(r'post_(\d+)', href)
                postID = int(re_match.group(1))
                url = "{}{}/{}/post_{}.html".format(baseUrl, int(postID / 1000000), int(postID / 1000), postID)
                result.append(url)
                
        return result
    
    
    def _getProjectID(self, pageNum = None) -> list:
        pageIndex = "_{}".format(pageNum) if pageNum != 1 else ""
        # url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/index{}.html'.format(pageIndex)
        # url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/yfl/index{}.html'.format(pageIndex) # 粤府令
        # url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/yf//index{}.html'.format(pageIndex) # 粤府
        # url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/yfh/index{}.html'.format(pageIndex) # 粤府函
        # url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/yfb/index{}.html'.format(pageIndex) # 粤府办
        url = 'https://www.gd.gov.cn/zwgk/wjk/qbwj/ybh/index{}.html'.format(pageIndex) # 粤办函

        rowData = requests.get(url).text
        fileList = self.__getFileUrl(rowData)
        return fileList

    def _getRowData(self, projectID, rowData = None) -> dict:
        url = projectID
        rowData = {
            'projectID': projectID,
            'rowPage': requests.get(url).text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = GuangdongGovExtractor()
        return extractor.extractGuangdongGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
