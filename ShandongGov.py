from ShandongGovSpider.ShanDongGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    ShandongGov = db['ShandongGov']
    
    spider = ShandongGovSpider(ShandongGov)
    
    # rowData = spider._getRowData('http://www.shandong.gov.cn/jpaas-jpolicy-web-server/front/info/detail?iid=ec18431daf18484d923806f49764b4f4')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 71)
