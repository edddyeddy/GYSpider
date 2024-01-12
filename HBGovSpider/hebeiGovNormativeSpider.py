from HBGovSpider.hebeiGovSpider import *

class hebeiGovNormativeSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://info.hebei.gov.cn/hbszfxxgk/6898876/7026469/7026511/7026505/f8f81d0a/index{}.html'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
