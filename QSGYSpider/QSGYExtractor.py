from QSGYSpider.QSGYStructure import *
import time

class QSGYExtractor(object):
    """
    轻松公益信息提取
    """

    def __init__(self, projectID, info, feed, extra) -> None:
        self.projectID = projectID
        self.info = info
        self.feed = feed
        self.extra = extra

    def getFundingInfo(self):
        fundingInfo = createFunding()
        fundingInfo['targetMoney'] = self.info.get('data').get("total_amount")
        fundingInfo['receivedMoney'] = self.info.get(
            'data').get("current_amount")
        fundingInfo['backerCount'] = self.info.get('data').get("backer_count")
        fundingInfo['shareCnt'] = self.info.get('data').get("share_count")
        return fundingInfo

    def getOrganizationInfo(self):
        orgInfo = createOrganization()
        orgInfo['executionOrg'] = self.extra.get(
            'data').get('execution_organization').get('name')
        orgInfo['publishOrg']['name'] = self.extra.get(
            'data').get('publish_organization').get('name')
        orgInfo['publishOrg']['socialCreditNo'] = self.extra.get(
            'data').get('publish_organization').get('social_credit_no')
        orgInfo['publisher'] = self.extra.get(
            'data').get('publisher').get('name')
        orgInfo['receiver'] = self.extra.get(
            'data').get('receive_fund').get('name')
        return orgInfo

    def getDescriptionInfo(self):
        descInfo = createDescription()
        descInfo['title'] = self.info.get('data').get('title')
        descInfo['rowDesc'] = self.info.get('data').get('detail')
        descInfo['cate'] = self.info.get('data').get('tag_name')
        feedback = self.feed.get('data').get("topics")
        if feedback != None:
            descInfo['feedBackCount'] = len(feedback)

        return descInfo

    def getData(self):
        data = {
            "projectID": None,
            "funding": None,
            "organization": None,
            "description": None,
            "collectTime": time.time()
        }
        data['projectID'] = self.projectID
        data['funding'] = self.getFundingInfo()
        data['organization'] = self.getOrganizationInfo()
        data['description'] = self.getDescriptionInfo()

        return data
