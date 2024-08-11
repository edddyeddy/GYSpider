from bs4 import BeautifulSoup
import re

class QinghaiGovExtractor(object):
    """
    青海政府数据提取
    """
    
    def extractQinghaiGovData(self, rowData):
        """
        提取青海政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__QinghaiGovInfo()
        
        titleSoup = BeautifulSoup(soup.find(attrs={"name": "ArticleTitle"})['content'],'lxml')
        data['title'] = titleSoup.text
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        # # 从内容中获取发布日志
        # pattern = r'（(?:\d{4}年\d{1,2}月\d{1,2}日.*?)+）'
        # sub_title = soup.find(attrs={"class": "con-subtit"})
        # match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', sub_title.text)
        # year, month, day = match.groups()
        # formatted_date = f'{year}-{int(month):02d}-{int(day):02d}'
        # data['pubDate'] = formatted_date
        # print(data['pubDate'])
        
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"class": "con-article"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "zp lf"})
        data['content'] = contentSoup.text

        return data

    def __QinghaiGovInfo(self):
        """
        青海政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
