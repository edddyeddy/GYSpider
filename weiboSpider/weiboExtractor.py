class weiboExtractor(object):
    """
    微博数据提取
    """
    def extractWeiboData(self,rowData):
        """
        提取微博数据
        """
        data = self.__weiboInfo()
        data['projectID'] = rowData['projectID']
        data['name'] = rowData['rowData']['user']['screen_name']
        data['weiboCount'] = rowData['rowData']['user']['statuses_count']
        data['followers'] = rowData['rowData']['user']['followers_count']
        data['isVerified'] = rowData['rowData']['user']['verified']
        data['getTime'] = rowData['getTime']

        return data

    def __weiboInfo(self):
        """
        微博数据结构
        """
        ret = {
            "projectID" :None,
            "name":None,
            "weiboCount":None,
            "followers":None,
            "isVerified":None,
            "getTime":None,
        }

        return ret