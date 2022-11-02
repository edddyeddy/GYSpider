def createCate():
    cate = {
        "cateID": None,
        "cateName": None
    }
    return cate


def createSubCate():
    subCate = {
        "subCateID": None,
        "subCateName": None
    }
    return subCate


def createObjCate():
    objCate = {
        "ObjCateID": None,
        "ObjCateName": None
    }
    return objCate


def createCateInfo():
    cateInfo = {
        "cate": createCate(),
        "subCate": createSubCate(),
        "objCate": createObjCate()
    }
    return cateInfo


def createDescInfo():
    descInfo = {
        "title": None,
        "summery": None,
        "desc": None,
        "rowDesc": None
    }
    return descInfo


def createFundingInfo():
    fundingInfo = {
        "targetMoney": None,
        "receivedMoney": None,
        "donateTimes": None
    }
    return fundingInfo


def createLocationInfo():
    locationInfo = {
        "province": None,
        "city": None,
        "cityCode": None
    }
    return locationInfo


def createPlanInfo():
    planInfo = {
        "plan": None,
        "budget": None,
    }
    return planInfo


def createBasicInfo():
    basicInfo = {
        "cateInfo": createCateInfo(),
        "descInfo": createDescInfo(),
        "fundingInfo": createFundingInfo(),
        "locationInfo": createLocationInfo(),
        "planInfo": createPlanInfo(),
        "recordNumber": None
    }
    return basicInfo


def createFunderInfo():
    funderInfo = {
        "funderName": None,
        "funderCorp": None,
        "funderIntro": None
    }
    return funderInfo


def createOrgInfo():
    orgInfo = {
        "OrgName": None,
        "funderInfo": createFunderInfo(),
        "capability": None,
        "orgIntro": None,
        "supportOrg": None
    }
    return orgInfo


def createTimeInfo():
    timeInfo = {
        "launchTime": None,
        "startTime": None,
        "endTime": None,
        "collectTime": None,
        "status": None
    }
    return timeInfo


def createProgressContent():
    progressContent = {
        "progressTitle": None,
        "progressDesc": None,
        "createTime": None
    }
    return progressContent


def createProgressInfo():
    progressInfo = {
        "progressNum": None,
        "progressList": None
    }
    return progressInfo


def createEmotionInfo():
    emotionInfo = {
        "sentiment": None,
        "emotion": None
    }
    return emotionInfo


def createProjectInfo():
    projectInfo = {
        "projectID": None,
        "basicInfo": createBasicInfo(),
        "orgInfo": createOrgInfo(),
        "timeInfo": createTimeInfo(),
        "progressInfo": createTimeInfo()
    }
    return projectInfo
