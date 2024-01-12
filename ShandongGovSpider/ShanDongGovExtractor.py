from bs4 import BeautifulSoup

class ShandongGovExtractor(object):
    """
    山东政府数据提取
    """
    
    def extractShandongGovData(self, rowData):
        """
        提取山东政府数据
        """
        data = self.__shandongGovInfo()
        soup = BeautifulSoup(rowData['rowPage'],'lxml')

        data['url'] = rowData['url']
        data['content'] = soup.find(attrs={"class": "main_content"}).text
        data['title'] = rowData['rowInfo']['title']
        data['pubDate'] = rowData['rowInfo']['publishDate']

        return data

    def __shandongGovInfo(self):
        """
        山东政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
