from bs4 import BeautifulSoup
import re

class HainanGovExtractor(object):
    """
    海南政府数据提取
    """
    
    def extractHainanGovData(self, rowData):
        """
        提取海南政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__HainanGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        
        # 规章的日期要从内容中获取
        # date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        # all_p_tag = soup.find_all('p')
        # for p in all_p_tag:
        #     pattern = p.text
        #     dates = re.findall(date_pattern, pattern)
        #     if dates:
        #         last_date = dates[0]
        #         data['pubDate'] = f"{last_date[0]}-{int(last_date[1]):02d}-{int(last_date[2]):02d}"
        # print(data['pubDate'])
        
        
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "xgleft"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "dbj-nr-m"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "cen_box"})
        data['content'] = contentSoup.text
        
        return data

    def __HainanGovInfo(self):
        """
        海南政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
