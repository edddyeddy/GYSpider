from BJGovSpider.BeiJingGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    BeiJingGov = db['BeiJingGovOffice']
    
    spider = BeiJingGovSpider(BeiJingGov)
    
    # rowData = spider._getRowData('https://www.beijing.gov.cn/zhengce/zfwj/zfwj/bgtwj/201905/t20190523_75324.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # urls = spider._saveProjectIDPeriodically(1000)
    # print(urls)
    
    # spider.updateProjectDataPeriodically(1000000)
    spider._extractProjectDataPeriodically(100000)
    
    # spider.scrapeAllProjectDataByPage(1, 236)
