from SDCSpider.SDCSpider import *
import pymongo

def cntProjectNum(uuid , col):
    cnt = 0
    for item in col.find({'projectID':uuid}):
        cnt += 1
    return cnt

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    sdc = db['QingSongChou']
    
    dupSet = set()
    removeSet = list()
    for project in sdc.find():
        projectID = project['projectID']
        if cntProjectNum(projectID ,sdc) > 1:
            dupSet.add(projectID)
            print(projectID)
    cnt = 0
    for uuid in dupSet:
        query = {
            'projectID':uuid,
            'rowData':{'$exists':False}
        }
        for item in sdc.find(query): 
            id = item['_id']
            removeSet.append(id)
            # sdc.delete_one({'_id':id})
            break
        
    print(removeSet)
    print(len(removeSet))
    print(len(dupSet))
        