from bs4 import BeautifulSoup

class BeiJingGovExtractor(object):
    """
    北京市政府数据提取
    """
    
    def extractBeiJingGovData(self, rowData):
        """
        提取北京市政府数据
        """
        data = self.__BeiJingGovInfo()
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')
        
        data['url'] = rowData['projectID']
        data['title'] = soup.find(attrs={"name":"ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name":"PubDate"})['content'].split(' ')[0]
        data['content'] = soup.find(attrs={"id":"mainText"}).text
        
        return data

    def __BeiJingGovInfo(self):
        """
        北京市政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
