from bs4 import BeautifulSoup

class JilinGovExtractor(object):
    """
    吉林政府数据提取
    """
    
    def extractJilinGovData(self, rowData):
        """
        提取吉林政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__JilinGovInfo()
        
        data['title'] = soup.title.text
        data['pubDate'] = rowData['pubData']
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"class": "content"}) 
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "contents_div"}) 
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "Custom_UnionStyle"}) 
        data['content'] = contentSoup.text
        # print(data)
        return data

    def __JilinGovInfo(self):
        """
        吉林政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
