from JDSpider.JDSpider import *
import pymongo

if __name__ == "__main__":

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    collection = db['JingDong']

    spider = JDSpider(collection)

    spider.scrapeAllProjectDataByPage(1, 12)
