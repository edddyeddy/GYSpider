from HBGovSpider.hebeiGovNormativeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    HebeiGovNormativeCol = db['HebeiGovNormative']
    
    spider = hebeiGovNormativeSpider(HebeiGovNormativeCol)
    
    # rowData = spider._getRowData('https://info.hebei.gov.cn/hbszfxxgk/6898876/7026513/7026522/7078965/index.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 5)
