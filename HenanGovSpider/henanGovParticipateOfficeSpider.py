from HenanGovSpider.henanGovSpider import *

class henanGovParticipateOfficeSpider(henanGovSpider):
    def _getProjectID(self, pageNum) -> list:
        return self._getHenanGovFileList(pageNum, self.CHANNEL_PARTICIPATE_OFFICE)