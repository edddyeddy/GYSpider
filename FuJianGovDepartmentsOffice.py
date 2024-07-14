from FJGovSpider.FujianGovDepartmentsOfficeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    FujianGovDepartments = db['福建省_省政府办行政规范性文件']
    
    spider = FujianGovDepartmentsOfficeSpider(FujianGovDepartments)
    
    # pageLinks = spider._getProjectID(1)
    # print(pageLinks)
    
    # row_data = spider._getRowData('https://www.fujian.gov.cn/zwgk/zfxxgk/szfwj/jgzz/xzgfxwj/202211/t20221128_6064165.htm')
    # print(spider._extractData(row_data))
    
    spider.scrapeAllProjectDataByPage(1, 34)
