from bs4 import BeautifulSoup

class YunNanGovExtractor(object):
    """
    云南政府数据提取
    """
    
    def extractYunNanGovData(self, rowData):
        """
        提取云南政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'],'lxml')
        
        data = self.__YunNanGovInfo()
        
        data['title'] = soup.find(attrs={"name": "articletitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "pubdate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        # data['column'] = soup.find(attrs={"name": "columntype"})['content']
        # 政策文件需要提取文号
        table_soup = soup.find(attrs={"class": "referencebox"})
        reference_soup = table_soup.find_all(attrs={"class": "reference"})
        for reference in reference_soup:
            if '文号' in reference.dt.text:
                wenhao_text = reference.dd.text
        data['column'] = wenhao_text.split('〔')[0].strip()
        print(data['column'])

        contentSoup = soup.find(attrs={"class": "arti"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "view TRS_UEDITOR trs_paper_default trs_web trs_key4format"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "view TRS_UEDITOR trs_paper_default trs_web"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "trs_editor_view TRS_UEDITOR trs_paper_default trs_web"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "trs_editor_view TRS_UEDITOR trs_paper_default trs_external trs_web trs_key4format"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "view TRS_UEDITOR trs_paper_default trs_web trs_word"})
       
       
        data['content'] = contentSoup.text
        
        return data

    def __YunNanGovInfo(self):
        """
        云南政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None,
            'column':None,
        }
        return ret
