from HBGovSpider.hebeiGovSpider import *

class hebeiGovOtherSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://info.hebei.gov.cn/hbszfxxgk/6898876/6934675/6998412/7043501/40df4e08/index{}.html'
        attrs = {'class': 'xxgkzclbtab3'}
        return self._getProjectIDByType(pageNum, url, attrs)
