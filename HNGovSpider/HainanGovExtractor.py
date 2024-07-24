from bs4 import BeautifulSoup
import re

class HainanGovExtractor(object):
    """
    海南政府数据提取
    """
    
    def extractHainanGovData(self, rowData):
        """
        提取海南政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__HainanGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "xgleft"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "dbj-nr-m"})
        data['content'] = contentSoup.text
        
        return data

    def __HainanGovInfo(self):
        """
        海南政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
