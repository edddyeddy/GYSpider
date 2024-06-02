from HBGovSpider.hebeiGovSpider import *

class hebeiGovOtherSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.hebei.gov.cn/columns/84f73ef0-6a8d-495e-9bf2-acffc68c31f6/templates/09a19324-88df-4949-b69b-f29b625e5e59/blocks/68261b4a-dac0-411d-95cf-5cef697b63d7?page={}&fix=0'
        attrs = {'class': 'xxgk_gfxwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
