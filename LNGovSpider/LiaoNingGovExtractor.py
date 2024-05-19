from bs4 import BeautifulSoup

class LiaoningGovExtractor(object):
    """
    辽宁政府数据提取
    """
    
    def extractLiaoningGovData(self, rowData):
        """
        提取辽宁政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__LiaoningGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content']
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"class": "content"}) # 其他选这个
        # contentSoup = soup.find(attrs={"class": "content1"}) # 部门文件选择这个

        data['content'] = contentSoup.text
        
        return data

    def __LiaoningGovInfo(self):
        """
        辽宁政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
