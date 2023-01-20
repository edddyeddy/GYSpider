from SDCSpider.SDCStructure import *
import time

class SDCExtractor(object):
    """
    水滴筹信息提取
    """

    def __init__(self, base, verify, caseLabels, withdraw, userCase):
        self.base = base
        self.verify = verify
        self.caseLabels = caseLabels
        self.withdraw = withdraw
        self.userCase = userCase
        
    def getDebtRangeType(self, debtType, homeDebt):
        if debtType == None:
            # 超过分类上限返回为7,没有负债返回0
            return 7 if homeDebt else 0
        return debtType
    
    def getDictVal(self, target, path):
        """
        获取字典中的数据,若不存在则返回None
        """
        for key in path:
            if target == None:
                return None
            target = target.get(key)
        
        return target
    
    def getFunding(self):
        funding = createFunding()
        
        funding['targetMoney'] = self.getDictVal(self.base,['data','baseInfo','targetAmount'])
        funding['receivedMoney'] = float(self.getDictVal(self.userCase,['data','caseBaseInfo','amount'])) / 100
        funding['donateCount'] = self.getDictVal(self.userCase,['data','caseBaseInfo','donateCount'])
        funding['ShareCount'] = self.getDictVal(self.userCase,['data','caseBaseInfo','shareCount'])
        funding['startTime'] = self.getDictVal(self.base,['data','baseInfo','startTime'])
        funding['finishTime'] = self.getDictVal(self.base,['data','baseInfo','endTime'])
        funding['withdrawCount'] = len(self.getDictVal(self.withdraw,['data','records']))
        
        funding['startTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(funding['startTime']) / 1000))
        funding['finishTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(funding['finishTime']) / 1000))
        
        return funding

    def getPublisher(self):
        publisher = createPublisher()
        
        publisher['name'] = self.getDictVal(self.base,['data','baseInfo','name'])
        publisher['age'] = self.getDictVal(self.base,['data','baseInfo','age'])
        publisher['disease'] = self.getDictVal(self.base,['data','paySuccessPageVO'])
        publisher['relationship'] = self.getDictVal(self.base,['data','customRelationDesc'])
        publisher['proofCount'] = self.getDictVal(self.verify,['data','count'])
        publisher['province'] = self.getDictVal(self.base,['data','baseInfo','provinceName'])
        publisher['labels'] = self.caseLabels
         
        return publisher

    def getDescription(self):
        description = createDescription()
        
        description['title'] = self.getDictVal(self.base,['data','baseInfo','title'])
        description['rowDesc'] = self.getDictVal(self.base,['data','baseInfo','content'])
        description['imageCount'] = len(self.getDictVal(self.base,['data','treatmentInfo','attachments'])) + len(self.getDictVal(self.base,['data','baseInfo','attachments']))
        description['feedBackCount'] = len(self.getDictVal(self.base,['data','fundUseDetails']))

        return description

    def getBasicInformation(self):
        basicInformation = createBasicInformation()
        
        basicInformation['selfBuiltHouse'] = self.getDictVal(self.base,['data','insuranceModelVo','selfBuiltHouse','totalCount'])
        basicInformation['houseProperty'] = self.getDictVal(self.base,['data','insuranceModelVo','houseProperty','totalCount'])
        basicInformation['car'] = self.getDictVal(self.base,['data','insuranceModelVo','carProperty','totalCount'])
        basicInformation['homeDebt'] = self.getDictVal(self.base,['data','insuranceModelVo','homeDebt'])
        basicInformation['homeDebtRangeType'] = self.getDebtRangeType(self.getDictVal(self.base,['data','insuranceModelVo','homeDebtRangeType']),basicInformation['homeDebt'])
        basicInformation['homeIncomeRangeType'] = self.getDictVal(self.base,['data','insuranceModelVo','homeIncomeRangeType'])
        basicInformation['medicalInsurance'] = self.getDictVal(self.base,['data','insuranceModelVo','medicalInsurance'])
        basicInformation['lifeInsurance'] = self.getDictVal(self.base,['data','insuranceModelVo','lifeInsurance'])
        basicInformation['propertyInsurance'] = self.getDictVal(self.base, ['data', 'insuranceModelVo', 'propertyInsurance'])
        basicInformation['otherPlatform'] = self.getDictVal(self.base,['data','insuranceModelVo','otherPlatform','hasRaise'])

        return basicInformation

    def getProjectInfo(self):

        projectInfo = {
            "publisher": self.getPublisher(),
            "funding": self.getFunding(),
            "description": self.getDescription(),
            "basicInformation": self.getBasicInformation(),
        }

        return projectInfo