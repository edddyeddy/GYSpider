from bs4 import BeautifulSoup

class ShanxiGovExtractor(object):
    """
    山西政府数据提取
    """
    
    def extractShanxiGovData(self, rowData):
        """
        提取山西政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__ShanxiGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"class": "sxgzk-detail-con"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "container boxcenter sxszf-detail"})
        data['content'] = contentSoup.text
        
        
        return data

    def __ShanxiGovInfo(self):
        """
        山西政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
