from SDCSpider.SDCSpider import *
import threading
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    sdc = db['ShuiDiChou']
    
    auth = '1BkW8Nt5KE9tqTAYguX7eCCxBjsZ5ivEI5VtFRjUhoE='
    spider = SDCSpider(auth,sdc)

    targetList = [spider.saveProjectIDPeriodically,
                  spider.updateProjectDataPeriodically,
                  spider.extractProjectDataPeriodically]

    for target in targetList:
        threading.Thread(target=target).start()
        time.sleep(20)

