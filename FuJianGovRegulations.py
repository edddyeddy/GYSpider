from FJGovSpider.FujianGovRegulations import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    fujianGov = db['FuJian']
    
    spider = FujianGovRegulationsSpider(fujianGov)
    
    # pageLinks = spider._getProjectID(1)
    row_data = spider._getRowData('https://www.fujian.gov.cn/zwgk/zfxxgk/zfxxgkzc/fjsgzk/202112/t20211216_5794806.htm')
    print(spider._extractData(row_data))
    
    # spider.scrapeAllProjectDataByPage(1,25)
