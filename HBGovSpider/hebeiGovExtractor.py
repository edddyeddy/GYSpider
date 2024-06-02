from bs4 import BeautifulSoup

class hebeiGovExtractor(object):
    """
    河北政府数据提取
    """
    
    def extractHenanGovData(self, rowData):
        """
        提取河北政府数据
        """
        data = self.__hebeiGovInfo()
        rowPage = rowData['rowPage']
        
        soup = BeautifulSoup(rowPage, "lxml")
        
        data['url'] = rowData['projectID']
        data['title'] = soup.title.text
        data['pubDate'] = soup.find(attrs={"name": "PubDate"}).get('content')
    
        contentSoup =  soup.find(attrs={"class": "xxgk_gfxwjk-xqy-neir"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "xxgkgzwjk_xqy-cont"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "incontent"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"id": "zoom"})
        data['content'] = contentSoup.text

        return data

    def __hebeiGovInfo(self):
        """
        河北政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
