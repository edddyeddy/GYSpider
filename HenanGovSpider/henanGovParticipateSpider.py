from HenanGovSpider.henanGovSpider import *

class henanGovParticipateSpider(henanGovSpider):
    def _getProjectID(self, pageNum) -> list:
        return self._getHenanGovFileList(pageNum, self.CHANNEL_PARTICIPATE)