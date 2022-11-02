from QSCSpider.QSCSpider import *
import threading
import pymongo
import time

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    qsc = db['QingSongChou']

    spider = QSCSpider(qsc)
    targetList = [spider.saveProjectIDPeriodically,
                  spider.extractProjectDataPeriodically,
                  spider.updateProjectData]

    for target in targetList:
        threading.Thread(target=target).start()
        time.sleep(20)
