from HBGovSpider.hebeiGovSpider import *

class hebeiGovOfficeOtherSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.hebei.gov.cn/columns/8dff597e-a95c-4b20-b321-a5320af40141/templates/09a19324-88df-4949-b69b-f29b625e5e59/blocks/68261b4a-dac0-411d-95cf-5cef697b63d7?page={}&fix=0'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
