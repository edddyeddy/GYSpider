from TencentSpider.TencentSpider import *
import pymongo
import time

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    tencent = db['Tencent']

    spider = TencentSpider(tencent)

    spider.scrapeAllProjectDataByID(1,3000003)