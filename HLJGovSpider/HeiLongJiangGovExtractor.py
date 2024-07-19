from bs4 import BeautifulSoup


class HeilongjiangGovExtractor(object):
    """
    黑龙江政府数据提取
    """

    def extractHeilongjiangGovData(self, rowData):
        """
        提取黑龙江政府数据
        """
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')

        data = self.__HeilongjiangGovInfo()

        data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
        data['pubDate'] = soup.find(attrs={"name": "PubDate"})[
            'content'].split(' ')[0]
        data['url'] = rowData['projectID']
        data['column'] = soup.find(attrs={"name": "ColumnName"})['content']
        contentSoup = soup.find(attrs={"class": "gzk_detail"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "article_content article_content_body"})
        data['content'] = contentSoup.text

        return data

    def __HeilongjiangGovInfo(self):
        """
        黑龙江政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate': None,
            'column': None,
        }
        return ret
