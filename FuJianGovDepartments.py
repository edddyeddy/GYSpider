from FJGovSpider.FujianGovDepartmentsSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    FujianGovDepartments = db['FujianGovDepartments']
    
    spider = FujianGovDepartmentsSpider(FujianGovDepartments)
    
    # pageLinks = spider._getProjectID(10)
    # print(pageLinks)
    
    # row_data = spider._getRowData('https://sft.fujian.gov.cn/zwgk/zfxxgkzl/zfxxgkml/xzgfxwj/201109/t20110902_3040015.htm')
    # print(spider._extractData(row_data))
    
    spider.scrapeAllProjectDataByPage(1, 434)
