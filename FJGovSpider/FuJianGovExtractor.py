from bs4 import BeautifulSoup
from datetime import datetime
import re

class FujianGovExtractor(object):
    """
    福建政府数据提取
    """
    

    def extractFujianGovData(self, rowData):
        """
        提取福建政府数据
        """
        data = self.__FujianGovInfo()
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')
        
        contentSoup = soup.find(attrs={"class": "Custom_UnionStyle"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"id": "trsContent"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "TRS_Editor"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "tabs tab_base_01 rules_con1"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "article_component"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"id": "detailCont"})
        
        data['content'] = contentSoup.text.strip()
        data['url'] = rowData['url']
        
        titleSoup = soup.find(attrs={"name":"ArticleTitle"})
        if titleSoup is None:
            titleSoup = soup.find(attrs={"class": "rules_tit"})
        if titleSoup is None:
            titleSoup = soup.find(attrs={"class": "article_title text_align_center"})
        
        data['title'] = titleSoup['content']

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

    def __FujianGovInfo(self):
        """
        福建政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'publish':None,
        }
        return ret
