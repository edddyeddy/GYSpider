from bs4 import BeautifulSoup

class TianJinGovExtractor(object):
    """
    天津市政府数据提取
    """
    
    def extractTianJinGovData(self, rowData):
        """
        提取天津市政府数据
        """
        data = self.__TianJinGovInfo()
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')
        
        data['url'] = rowData['projectID']
        data['title'] = soup.find(attrs={"name":"ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name":"PubDate"})['content'].split(' ')[0]
        data['content'] = soup.find(attrs={"id":"xlrllt"}).text
        
        return data

    def __TianJinGovInfo(self):
        """
        天津市政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
