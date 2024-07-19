from bs4 import BeautifulSoup

class ZhejiangGovExtractor(object):
    """
    浙江政府数据提取
    """
    
    def extractZhejiangGovData(self, rowData):
        """
        提取浙江政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__ZhejiangGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "zc_article_con"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "bt_content"})
        data['content'] = contentSoup.text
        
        return data

    def __ZhejiangGovInfo(self):
        """
        浙江政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
