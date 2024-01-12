from HenanGovSpider.henanGovSpider import *

class henanGovOtherSpider(henanGovSpider):
    def _getProjectID(self, pageNum) -> list:
        return self._getHenanGovFileList(pageNum, self.CHANNEL_GOV_OTHER)