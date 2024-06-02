from HBGovSpider.hebeiGovSpider import *

class hebeiGovRegulationsSpider(hebeiGovSpider):
    def _getProjectID(self, pageNum) -> list:
        url = 'https://www.hebei.gov.cn/columns/e4a82431-5daf-4e1f-b7ff-80a68ad951b2/templates/06113b1b-3575-4358-b511-39028e54a12c/blocks/92c271ad-8bba-4a4d-9e7f-3af5efb2842b?page={}&fix=0'
        attrs = {'class': 'xxgkgzwjk-list-li'}
        return self._getProjectIDByType(pageNum, url, attrs)
        # url = 'https://www.hebei.gov.cn/columns/e4a82431-5daf-4e1f-b7ff-80a68ad951b2/templates/06113b1b-3575-4358-b511-39028e54a12c/blocks/92c271ad-8bba-4a4d-9e7f-3af5efb2842b?page={}&fix=0'.format(pageNum)
        # return self._getProjectIDByURL(url)