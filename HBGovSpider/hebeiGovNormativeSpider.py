from HBGovSpider.hebeiGovSpider import *

class hebeiGovNormativeSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.hebei.gov.cn/columns/b1b59c8c-81a3-4cf2-b876-8618919c0049/templates/2e3e81cf-d53a-40f0-9d7f-060e77400269/blocks/c0704ccb-1df3-4edd-9391-3f0e6d7db920?page={}&fix=0'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
