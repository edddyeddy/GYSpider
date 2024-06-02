from HBGovSpider.hebeiGovSpider import *

class hebeiGovOfficeNormativeSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.hebei.gov.cn/columns/3d33a20b-4271-4b3b-8cae-3664e980d262/templates/2e3e81cf-d53a-40f0-9d7f-060e77400269/blocks/c0704ccb-1df3-4edd-9391-3f0e6d7db920?page={}&fix=0'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
