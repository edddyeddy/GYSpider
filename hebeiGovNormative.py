from HBGovSpider.hebeiGovNormativeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    HebeiGovNormativeCol = db['河北_行政规范_省政府']
    
    spider = hebeiGovNormativeSpider(HebeiGovNormativeCol)
    
    # rowData = spider._getRowData('https://www.hebei.gov.cn/columns/b1b59c8c-81a3-4cf2-b876-8618919c0049/202308/15/6f1b4180-6013-4094-9930-e36fbdaf230f.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 5)
