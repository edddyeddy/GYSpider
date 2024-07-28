from SCGovSpider.SiChuanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['四川省_规章']
    
    spider = SichuanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.sc.gov.cn/10462/c108923/2017/11/28/1174702c3bdd47ccad16e5346cea6a47.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 11)
