from HBGovSpider.hebeiGovSpider import *

class hebeiGovOfficeNormativeSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://info.hebei.gov.cn/hbszfxxgk/6898876/7026469/7026511/7026506/b9e089db/index{}.html'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
