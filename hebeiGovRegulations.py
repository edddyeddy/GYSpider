from HBGovSpider.hebeiGovRegulationsSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    HebeiGovRegulationsCol = db['HebeiGovRegulations']
    
    spider = hebeiGovRegulationsSpider(HebeiGovRegulationsCol)
    
    # rowData = spider._getRowData('https://info.hebei.gov.cn/hbszfxxgk/6898876/6985862/6998354/index.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 14)
