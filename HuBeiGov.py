from HuBeiGovSpider.HubeiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['湖北省_规章']
    
    spider = HubeiGovSpider(col)
    
    # rowData = spider._getRowData('https://www.jiangxi.gov.cn/art/2022/12/20/art_4975_4305729.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    urls = spider._getProjectID(1)
    print(len(urls))
    print(urls)
    
    # spider.scrapeAllProjectDataByPage(1, 5)
