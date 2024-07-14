from bs4 import BeautifulSoup


class ShandongGovExtractor(object):
    """
    山东政府数据提取
    """

    def extractShandongGovData(self, rowData):
        """
        提取山东政府数据
        """
        data = self.__shandongGovInfo()
        soup = BeautifulSoup(rowData['rowPage'], 'lxml')

        data['url'] = rowData['url']
        contentSoup = soup.find(attrs={"class": "main_content"})
        if contentSoup is None:
            contentSoup = soup.find(attrs={"class": "wz_zhuti"})
        data['content'] = contentSoup.text

        if 'rowInfo' in rowData:
            print(rowData)
            data['title'] = rowData['rowInfo']['title']
            data['pubDate'] = rowData['rowInfo']['publishDate']
        else:
            data['title'] = soup.find(attrs={"name": "ArticleTitle"})['content']
            data['pubDate'] = soup.find(attrs={"name": "PubDate"})['content'].split(' ')[0]
        return data

    def __shandongGovInfo(self):
        """
        山东政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate': None
        }
        return ret
