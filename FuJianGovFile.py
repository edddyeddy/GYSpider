from FJGovSpider.FujianGovFile import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    FujianGovDepartments = db['福建省_其他']
    
    spider = FujianGovFile(FujianGovDepartments)
    
    # pageLinks = spider._getProjectID(1)
    # print(pageLinks)
    
    # row_data = spider._getRowData('http://www.fujian.gov.cn/zwgk/zfxxgk/szfwj/jgzz/nlsyzcwj/201301/t20130105_1476783.htm')
    # print(spider._extractData(row_data))
    
    spider.scrapeAllProjectDataByPage(1, 35)
