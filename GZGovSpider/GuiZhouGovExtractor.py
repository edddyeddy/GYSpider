from bs4 import BeautifulSoup

class GuiZhouGovExtractor(object):
    """
    贵州政府数据提取
    """
    
    def extractGuiZhouGovData(self, rowData):
        """
        提取贵州政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__GuiZhouGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "DocHtmlCon Box"})
        data['content'] = contentSoup.text
        
        return data

    def __GuiZhouGovInfo(self):
        """
        贵州政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
