from QSCSpider.QSCStructure import *
import time


class QSCExtractor(object):
    """
    轻松筹变量提取
    """

    def __init__(self, required, extend, feed, publicity):
        self.required = required
        self.extend = extend
        self.feed = feed
        self.publicity = publicity

    def getFunding(self):
        funding = createFunding()

        
        

        funding['targetMoney'] = float(
            self.required['data']['project']['target_amount']) / 100.0
        funding['receivedMoney'] = float(
            self.required['data']['project']['raised_amount']) / 100.0
        funding['donateCount'] = self.getDictVal(self.required,['data','project','support_number'])
        funding['ShareCount'] = self.getDictVal(self.required,['data','project','share_number'])
        funding['publicTime'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(self.required['data']['project']['created'])))

        return funding

    def getPublisher(self):
        publisher = createPublisher()
        
        publisher['name'] = self.getDictVal(self.required,['data','publisher_info','patient_name'])
        publisher['age'] = self.getDictVal(self.required,['data','publisher_info','patient_age'])
        publisher['disease'] = self.getDictVal(self.required,['data','publisher_info','patient_disease'])
        publisher['relationship'] = self.getDictVal(self.required,['data','publisher_info','relation'])
        publisher['proofCount'] = self.getDictVal(self.extend,['data','prove_data','prove_total'])

        return publisher

    def getDescription(self):
        description = createDescription()

        description['title'] = self.getDictVal(self.required,['data','project','name'])
        description['rowDesc'] = self.getDictVal(self.required,['data','project','detail'])
        description['imageCount'] = len(
            self.required['data']['project']['cover'])
        description['feedBackCount'] = len(self.feed['data'])

        return description

    def getBasicInformation(self):
        basicInformation = createBasicInformation()

        basicInformation['drugCost'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','extra','raise_fund_use', 'drug_cost', 'have'])
        basicInformation['nurseCost'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','extra','raise_fund_use', 'nurse_cost', 'have'])

        basicInformation['businessInsurance'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','extra','business_insurance','have'])
        basicInformation['govAssistance'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','extra','gov_assistance','have'])
        basicInformation['otherInfo'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','extra','other_info','have'])
        basicInformation['car'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','family_property','car','have'])
        basicInformation['financial'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','family_property','financial','have'])
        basicInformation['house'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','family_property','house','have'])
        basicInformation['income'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','family_property','income'])
        basicInformation['overdraft'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','family_property','overdraft'])
        basicInformation['low_security'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','medical_security','low_security','have'])
        basicInformation['medical_insurance'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','medical_security','medical_insurance','have'])
        basicInformation['multi_platform_raise_fund'] = self.getDictVal(self.extend,['data','property_supplement','property_plus','medical_security','multi_platform_raise_fund','have'])

        return basicInformation

    def getProjectInfo(self):

        projectInfo = {
            "publisher": self.getPublisher(),
            "funding": self.getFunding(),
            "description": self.getDescription(),
            "basicInformation": self.getBasicInformation(),
        }

        return projectInfo

    def getDictVal(self, target, path):
        """
        获取字典中的数据,若不存在则返回None
        """
        for key in path:
            if target == None:
                return None
            target = target.get(key)
        
        return target
