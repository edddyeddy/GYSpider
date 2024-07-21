from bs4 import BeautifulSoup

class AnHuiGovExtractor(object):
    """
    安徽政府数据提取
    """
    
    def extractAnHuiGovData(self, rowData):
        """
        提取安徽政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__AnHuiGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "articleCon"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "gzk-article"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "wzcon j-fontContent"})
        data['content'] = contentSoup.text
        
        return data

    def __AnHuiGovInfo(self):
        """
        安徽政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
