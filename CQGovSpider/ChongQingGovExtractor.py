from bs4 import BeautifulSoup
import re

class ChongqingGovExtractor(object):
    """
    重庆政府数据提取
    """
    
    # def extractChongqingGovData(self, rowData):
    #     """
    #     提取重庆政府数据
    #     """
    #     print(rowData)
    #     rowPage = rowData['rowPage']['data']
    #     soup = BeautifulSoup(rowPage['html'],'lxml')
    #     data = self.__ChongqingGovInfo()
        
    #     data['title'] = rowPage['fileName']
    #     data['pubDate'] = rowPage['publishDate']
    #     data['url'] = rowData['projectID']
    #     # data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
    #     data['content'] = soup.text
        
    #     return data
    
    def extractChongqingGovData(self, rowData):
        """
        提取重庆政府数据
        """
        rowPage = rowData['rowPage']
        soup = BeautifulSoup(rowPage,'lxml')
        data = self.__ChongqingGovInfo()
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "document mt-1 mt-12"})
        data['content'] = contentSoup.text
        
        return data

    def __ChongqingGovInfo(self):
        """
        重庆政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
