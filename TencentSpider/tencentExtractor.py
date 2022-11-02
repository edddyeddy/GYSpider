from TencentSpider.tencentStructure import *
from bs4 import BeautifulSoup
import time

class TencentExtractor:

    def __init__(self, detail, proInfo, progress):
        self.detail = detail
        self.proInfo = proInfo
        self.progress = progress
        self.projectInfo = createProjectInfo()

    def getCate(self):
        cate = createCate()
        cate["cateID"] = self.detail["base"].get("cateId")
        cate["cateName"] = self.detail["base"].get("cateName")
        return cate

    def getSubCate(self):
        subCate = createSubCate()
        subCate["subCateID"] = self.detail["base"].get("cateTag")
        subCate["subCateName"] = self.detail["base"].get("cateTagName")
        return subCate

    def getObjCate(self):
        objCate = createObjCate()
        objCate["ObjCateID"] = self.detail["base"].get("objTag")
        objCate["ObjCateName"] = self.detail["base"].get("objTagName")
        return objCate

    def getCateInfo(self):
        cateInfo = createCateInfo()
        cateInfo["cate"] = self.getCate()
        cateInfo["subCate"] = self.getSubCate()
        cateInfo["objCate"] = self.getObjCate()
        return cateInfo

    def getDescInfo(self):
        descInfo = createDescInfo()
        descInfo["title"] = self.detail["base"].get("title")
        descInfo["summery"] = self.detail["base"].get("summary")
        rowDesc = self.detail["detail"].get("desc")
        descInfo["rowDesc"] = rowDesc
        if rowDesc != None:
            soup = BeautifulSoup(rowDesc, 'lxml')
            descInfo["desc"] = soup.get_text()

        return descInfo

    def getFundingInfo(self):
        fundingInfo = createFundingInfo()

        targetMoney = self.detail["base"].get("needMoney")
        self_money = self.proInfo["msg"]["stat"].get("self_money")
        children_money = self.proInfo["msg"]["stat"].get("children_money")
        self_times = self.proInfo["msg"]["stat"].get("self_times")
        children_times = self.proInfo["msg"]["stat"].get("children_times")

        if targetMoney != None:
            targetMoney = float(targetMoney)/100

        receivedMoney = None
        if self_money != None and children_money != None:
            receivedMoney = (float(self_money) + float(children_money))/100

        donateTimes = None
        if self_times != None and children_times != None:
            donateTimes = int(self_times) + int(children_times)

        fundingInfo["targetMoney"] = targetMoney
        fundingInfo["receivedMoney"] = receivedMoney
        fundingInfo["donateTimes"] = donateTimes

        return fundingInfo

    def getLocationInfo(self):
        locationInfo = createLocationInfo()
        locationInfo["province"] = self.detail["base"].get("proj_province")
        locationInfo["cityCode"] = self.detail["base"].get("city_code")
        locationInfo["city"] = self.detail["base"].get("proj_city")
        return locationInfo

    def getPlanInfo(self):
        planInfo = createPlanInfo()
        planInfo["plan"] = self.detail["base"].get("exe_plan")
        planInfo["budget"] = self.detail["base"].get("proj_budget")
        return planInfo

    def getBasicInfo(self):
        basicInfo = createBasicInfo()
        basicInfo["cateInfo"] = self.getCateInfo()
        basicInfo["descInfo"] = self.getDescInfo()
        basicInfo["fundingInfo"] = self.getFundingInfo()
        basicInfo["locationInfo"] = self.getLocationInfo()
        basicInfo["planInfo"] = self.getPlanInfo()
        basicInfo["recordNumber"] = self.detail["base"].get("record_num")
        return basicInfo

    def getFunderInfo(self):
        funderInfo = createFunderInfo()
        funder = self.detail["base"].get("funder")
        if funder != None:
            funderInfo["funderName"] = self.detail["base"]["funder"].get(
                "name")
            funderInfo["funderCorp"] = self.detail["base"]["funder"].get(
                "corp")
            funderInfo["funderIntro"] = self.detail["base"]["funder"].get(
                "intro")
        return funderInfo

    def getOrgInfo(self):
        orgInfo = createOrgInfo()
        orgInfo["funderInfo"] = self.getFunderInfo()
        orgInfo["OrgName"] = self.detail["base"].get("eOrgName")
        desc_module = self.detail["detail"].get("desc_module")
        if desc_module != None:
            orgInfo["capability"] = desc_module.get("proj_exe_content")
            orgInfo["orgIntro"] = desc_module.get("proj_team_info")
        orgInfo["supportOrg"] = self.detail["base"].get("fundName")
        return orgInfo

    def getTimeInfo(self):
        timeInfo = createTimeInfo()
        timeInfo["launchTime"] = self.detail["base"].get("launch_time")
        timeInfo["startTime"] = self.detail["base"].get("startTime")
        timeInfo["endTime"] = self.detail["base"].get("endTime")
        timeInfo["status"] = self.detail["base"].get("status")

        collectTime = self.proInfo.get("time")
        if collectTime != None:
            timeInfo["collectTime"] = time.strftime(
                "%Y-%m-%d", time.localtime(collectTime))
        return timeInfo

    def getProgressContent(self, rawData):
        progressContent = createProgressContent()
        progressContent["progressTitle"] = rawData.get("content_title")
        progressContent["progressDesc"] = rawData.get("desc")
        createTime = rawData.get("create_time")
        if createTime != None:
            progressContent["createTime"] = time.strftime(
                "%Y-%m-%d", time.localtime(int(createTime)))

        return progressContent

    def getProgressInfo(self):
        progressInfo = createProgressInfo()
        progressList = []

        info = self.progress["info"]

        if info != "":
            rawDataList = self.progress["info"].get("list")
            for rawData in rawDataList:
                progressList.append(self.getProgressContent(rawData))

            progressInfo["progressNum"] = info["pages"].get("total")
            progressInfo["progressList"] = progressList

        return progressInfo

    def getProjectInfo(self):
        projectInfo = createProjectInfo()
        projectInfo["projectID"] = int(self.detail["base"].get("id"))
        projectInfo["basicInfo"] = self.getBasicInfo()
        projectInfo["orgInfo"] = self.getOrgInfo()
        projectInfo["timeInfo"] = self.getTimeInfo()
        projectInfo["progressInfo"] = self.getProgressInfo()
        return projectInfo


def getProjectInfo(detail, proInfo, progress):
    project = TencentExtractor(detail, proInfo, progress)
    return project.getProjectInfo()
