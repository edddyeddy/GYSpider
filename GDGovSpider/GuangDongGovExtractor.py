from bs4 import BeautifulSoup

class GuangdongGovExtractor(object):
    """
    广东政府数据提取
    """
    
    def extractGuangdongGovData(self, rowData):
        """
        提取广东政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__guangdongGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"wzades": "正文"})
        if contentSoup is not None:
            data['content'] = contentSoup.text
            return data

        contentSoup = soup.find(attrs={"class": "article-content"})
        data['content'] = contentSoup.text
        
        return data

    def __guangdongGovInfo(self):
        """
        广东政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
