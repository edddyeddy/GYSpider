from HBGovSpider.hebeiGovSpider import *

class hebeiGovRegulationsSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://info.hebei.gov.cn/hbszfxxgk/6898876/6985862/5afa2bab/index{}.html'
        attrs = {'class': 'xxgkgzwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
