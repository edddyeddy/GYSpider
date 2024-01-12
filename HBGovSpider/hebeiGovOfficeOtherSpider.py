from HBGovSpider.hebeiGovSpider import *

class hebeiGovOfficeOtherSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://info.hebei.gov.cn/hbszfxxgk/6898876/6934675/6998412/7043504/d01c303b/index{}.html'
        attrs = {'class': 'xxgkzclbtab3'}
        return self._getProjectIDByType(pageNum, url, attrs)
