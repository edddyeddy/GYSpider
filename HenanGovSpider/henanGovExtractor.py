class henanGovExtractor(object):
    """
    河南政府数据提取
    """
    
    def extractHenanGovData(self, rowData):
        """
        提取河南政府数据
        """
        data = self.__henanGovInfo()
        rowPage = rowData['rowPage']
        data['url'] = rowData['url']
        data['title'] = rowPage['title']
        data['content'] = rowPage['content']
        data['pubDate'] = rowPage['pubDate'].split(' ')[0]
        
        return data

    def __henanGovInfo(self):
        """
        河南政府数据结构
        """
        ret = {
            'url': None,
            'title': None,
            'content': None,
            'pubDate':None
        }
        return ret
