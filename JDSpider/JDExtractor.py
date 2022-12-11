from JDSpider.JDStructure import *
import time

class JDExtractor(object):
    """
    京东公益信息提取
    """
    
    def __init__(self, base, desc, feedback, message):
        self.base = base
        self.desc = desc
        self.feedback = feedback
        self.message = message
    
    def getDictVal(self, target, path):
        """
        获取字典中的数据,若不存在则返回None
        """
        for key in path:
            if target == None:
                return None
            target = target.get(key)
        
        return target
    
    def getTargetMoney(self):
        targetMoney = 0
        taskList = self.base['data']['taskList']
        
        for task in taskList:
            targetMoney += task['targetMoney']
            
        return targetMoney

    def getFundingInfo(self):
        funding = createFunding()
        
        funding["targetMoney"] = self.getTargetMoney()
        funding["receivedMoney"] = self.getDictVal(self.base,["data","collectCount"])
        funding["suppliesQuantity"] = self.getDictVal(self.base,["data","totalQuantity"])
        funding["messageCnt"] = self.getDictVal(self.message,["data","total"])
              
        return funding
    
    def getPublisherInfo(self):
        publisher = createPublisher()
        
        publisher["area"] = self.getDictVal(self.base,["data","areaName"])
        publisher["publishOrg"] = self.getDictVal(self.base,["data","name"])
        publisher["executionOrg"] = self.getDictVal(self.base,["data","projectExecOrg"])
        publisher["recordID"] = self.getDictVal(self.base,["data","projectRecord"])
        
        return publisher
    
    def getDescriptionInfo(self):
        description = createDescription()
        
        description["title"] = self.getDictVal(self.base,["data","title"])
        description["rowDesc"] = self.getDictVal(self.desc,["data","details"])
        feedback = self.getDictVal(self.feedback,["data"])
        description["feedBackCount"] = 0 if feedback == None else len(feedback)
        
        return description
    
    def getProjectInfo(self):

        projectInfo = {
            "publisher": self.getPublisherInfo(),
            "funding": self.getFundingInfo(),
            "description": self.getDescriptionInfo(),
        }

        return projectInfo
    
    