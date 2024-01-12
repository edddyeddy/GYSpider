import pymongo

def getDebtRangeType(debtType, homeDebt):
    if debtType == None:
        # 超过分类返回为7,没有负债返回0
        return 7 if homeDebt else 0
    return debtType


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    sdc = db['ShuiDiChou']

    maxType = 0
    for project in sdc.find({'data': {'$exists': True}}):
        projectID = project['projectID']
        homeDebtRangeType = project['rowData']['base']['data']['insuranceModelVo']['homeDebtRangeType']
        debt = project['rowData']['base']['data']['insuranceModelVo']['homeDebt']
            
        query = {'projectID':projectID}
        data = {"$set": {"data.basicInformation.homeDebtRangeType": getDebtRangeType(homeDebtRangeType,debt)}}
        print(query)
        print(data)
        sdc.update_one(query,data)
