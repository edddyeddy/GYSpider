from bs4 import BeautifulSoup

class NeimengguGovExtractor(object):
    """
    内蒙古政府数据提取
    """
    
    def extractNeimengguGovData(self, rowData):
        """
        提取内蒙古政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__NeimengguGovInfo()
        
        titleSoup = BeautifulSoup(soup.find(attrs={"name": "ArticleTitle"})['content'],'lxml')
        data['title'] = titleSoup.text
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        data['url'] = rowData['projectID']
        contentSoup = soup.find(attrs={"class": "text"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"trs_editor_view TRS_UEDITOR trs_paper_default trs_word"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"view TRS_UEDITOR trs_paper_default trs_word"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"view TRS_UEDITOR trs_paper_default trs_web"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"view TRS_UEDITOR trs_paper_default trs_word trs_web"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"trs_editor_view TRS_UEDITOR trs_paper_default trs_word trs_web"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"view TRS_UEDITOR trs_paper_default trs_external"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"trs_editor_view TRS_UEDITOR trs_paper_default trs_external"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class":"view TRS_UEDITOR trs_paper_default trs_external trs_web"})
        
        if contentSoup is not None:
            data['content'] = contentSoup.text
        else:
            content_divs = soup.find_all('div', class_='ql_detailbro_content qgl_fontsize_box')
            for div in content_divs:
                text = ''
                for child in div.children:
                    if child.name != 'div' or 'cc_shangxiaye' not in child.get('class', []):
                        text += str(child.text)
                data['content'] = text.strip()
        
        return data

    def __NeimengguGovInfo(self):
        """
        内蒙古政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
