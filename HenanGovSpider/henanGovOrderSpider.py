from HenanGovSpider.henanGovSpider import *

class henanGovOrderSpider(henanGovSpider):
    def _getProjectID(self, pageNum) -> list:
        return self._getHenanGovFileList(pageNum, self.CHANNEL_GOV_ORDER)