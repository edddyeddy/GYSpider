from HBGovSpider.hebeiGovRegulationsSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    HebeiGovRegulationsCol = db['河北省规章']
    
    spider = hebeiGovRegulationsSpider(HebeiGovRegulationsCol)
    
    # rowData = spider._getRowData('https://www.hebei.gov.cn/columns/e4a82431-5daf-4e1f-b7ff-80a68ad951b2/202311/27/c8d508a6-d409-4320-b090-b2d91f311879.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 14)
