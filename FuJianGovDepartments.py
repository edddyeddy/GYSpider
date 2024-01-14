from FJGovSpider.FujianGovDepartmentsSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    fujianGov = db['FuJian']
    
    spider = FujianGovDepartmentsSpider(fujianGov)
    
    # pageLinks = spider._getProjectID(10)
    # print(pageLinks)
    
    row_data = spider._getRowData('https://gat.fujian.gov.cn/zfxxgk/zfxxgkml/gfxwjml/xxyx/202112/t20211216_5795056.htm')
    print(spider._extractData(row_data))
    
    # spider.scrapeAllProjectDataByPage(1,25)
