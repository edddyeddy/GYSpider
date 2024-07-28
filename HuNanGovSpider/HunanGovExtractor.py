from bs4 import BeautifulSoup
import re

class HunanGovExtractor(object):
    """
    湖南政府数据提取
    """
    
    def extractHunanGovData(self, rowData):
        """
        提取湖南政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__HunanGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        # data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
        #     'content'].split(' ')[0]
        
        # # 规章的日期要从内容中获取
        # date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        # all_p_tag = soup.find_all('p')
        # for p in all_p_tag:
        #     pattern = p.text
        #     dates = re.findall(date_pattern, pattern)
        #     if dates:
        #         last_date = dates[0]
        #         data['pubDate'] = f"{last_date[0]}-{int(last_date[1]):02d}-{int(last_date[2]):02d}"
        #         break
        # print(data['pubDate'])
        
        # 政府文件日期提取
        date_pattern = r'发文日期：(\d{4}-\d{2}-\d{2})'
        a1_soup = soup.find(attrs={"class": "a1"})
        matches = re.findall(date_pattern, a1_soup.text)
        data['pubDate'] = matches[0]
        print(data['pubDate'])
        
        
        
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "content"})
        data['content'] = contentSoup.text
        
        return data

    def __HunanGovInfo(self):
        """
        湖南政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
