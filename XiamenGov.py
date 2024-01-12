from XiamenGovSpider.xiamenGovSpider import *
import threading
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    xiamenGov = db['XiamenGov']
    
    spider = XiamenGovSpider(xiamenGov)
    # rowData = spider._getRowData('https://www.xm.gov.cn/zwgk/flfg/sfbwj/200808/t20080820_273152.htm')
    # data = spider._extractData(rowData)
    # print(data)
    
    pageLinks = spider._getProjectID(2)
    print(pageLinks)
    
    # spider.scrapeAllProjectDataByPage(1,25)
