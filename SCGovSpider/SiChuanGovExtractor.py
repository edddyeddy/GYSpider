from bs4 import BeautifulSoup
import re

class SichuanGovExtractor(object):
    """
    四川政府数据提取
    """
    
    def extractSichuanGovData(self, rowData):
        """
        提取四川政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__SichuanGovInfo()
        
        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = rowData['pubDate'].split()[0].replace('/', '.')
        
        # 规章的日期要从内容中获取
        # print(rowData['projectID'])
        # date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        # date_soup = soup.find(attrs={"class": "zfgztit_ssdate"})
        # for date_text in date_soup:
        #     pattern = date_text.text
        #     dates = re.findall(date_pattern, pattern)
        #     if dates:
        #         last_date = dates[0]
        #         data['pubDate'] = f"{last_date[0]}-{int(last_date[1]):02d}-{int(last_date[2]):02d}"
        #         break
        # if not data['pubDate']:
        #     all_p_tag = soup.find_all('p')
        #     for p in all_p_tag:
        #         pattern = p.text
        #         dates = re.findall(date_pattern, pattern)
        #         if dates:
        #             last_date = dates[0]
        #             data['pubDate'] = f"{last_date[0]}-{int(last_date[1]):02d}-{int(last_date[2]):02d}"
        #             break
            
        # print(data['pubDate'])
        
        # # 政府文件日期提取
        # date_pattern = r'发文日期：(\d{4}-\d{2}-\d{2})'
        # a1_soup = soup.find(attrs={"class": "a1"})
        # matches = re.findall(date_pattern, a1_soup.text)
        # data['pubDate'] = matches[0]
        # print(data['pubDate'])
        
        
        
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "content"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"id": "cmsArticleContent"})
        data['content'] = contentSoup.text
        
        return data

    def __SichuanGovInfo(self):
        """
        四川政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
