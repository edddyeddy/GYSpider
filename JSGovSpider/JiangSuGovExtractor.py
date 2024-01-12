from bs4 import BeautifulSoup

class JiangSuGovExtractor(object):
    """
    江苏省政府数据提取
    """
    
    def extractJiangSuGovData(self, rowData):
        """
        提取江苏省政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')

        data = self.__jiangsuGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        data['url'] = rowData['projectID']
        content_soup = soup.find(attrs={"class": "article_content"})
        if content_soup is None:
            content_soup = soup.find(attrs={"class": "Custom_UnionStyle"})
        if content_soup is None:
            content_soup = soup.find(attrs={"id": "zoom"}) 
        data['content'] = content_soup.text
        
        return data

    def __jiangsuGovInfo(self):
        """
        江苏省政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
