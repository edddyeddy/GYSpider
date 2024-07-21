from bs4 import BeautifulSoup
import re

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
        # data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
        #     'content'].split(' ')[0]
        # 规章要从内容中提取
        subTitleSoup = soup.find(attrs={"class": "zc_artice_tit1"})
        subTitle = soup.text
        date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        match = re.search(date_pattern, subTitle)
        year = match.group(1)
        month = match.group(2).zfill(2)  # 将月份填充为两位数
        day = match.group(3).zfill(2)    # 将日期填充为两位数
        formatted_date = f"{year}-{month}-{day}"
        data['pubDate'] = formatted_date
        
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
