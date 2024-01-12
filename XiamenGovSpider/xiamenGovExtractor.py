from bs4 import BeautifulSoup
from datetime import datetime
import re

class XiamenGovExtractor(object):
    """
    厦门政府数据提取
    """
    

    def extractXiamenGovData(self, rowData):
        """
        提取厦门政府数据
        """
        data = self.__xiamenGovInfo()
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')
        
        contentSoup = soup.find(attrs={"class": "Custom_UnionStyle"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"id": "trsContent"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "TRS_Editor"})
        
        data['content'] = contentSoup.text.strip()
        data['url'] = rowData['url']
        
        titleSoup = soup.find(attrs={"name":"ArticleTitle"})
        if titleSoup is None:
            titleSoup = soup.find(attrs={"class": "rules_tit"})
        if titleSoup is None:
            titleSoup = soup.find(attrs={"class": "article_title text_align_center"})
        
        data['title'] = titleSoup.text

        publishSoup = soup.find(attrs={"name":"PubDate"})
        if publishSoup is not None:
            data['publish'] = publishSoup['content']
        else:
            date_pattern = re.compile(r't(\d{8})')
            matchDate = re.search(date_pattern, data['url'])
            timestamp = matchDate.group(1)
            
            date_object = datetime.strptime(str(timestamp), '%Y%m%d')
            data['publish'] = date_object.strftime('%Y-%m-%d')
            
        return data

    def __xiamenGovInfo(self):
        """
        厦门政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'publish':None,
        }
        return ret
