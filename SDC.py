from SDCSpider.SDCSpider import *
import threading
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    sdc = db['ShuiDiChou']
    
    auth = 'wEKZgkKvTa5guwi5hrCOC-SCjbeQzbVo32PC2uXwUUE='
    spider = SDCSpider(auth,sdc)

    targetList = [spider.saveProjectIDPeriodically,
                  spider.updateProjectDataPeriodically]

    for target in targetList:
        threading.Thread(target=target).start()
        time.sleep(20)

