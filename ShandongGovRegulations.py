from ShandongGovSpider.ShanDongGovRegulationSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    ShandongGov = db['山东省_规章']
    
    spider = ShanDongGovRegulationSpider(ShandongGov)
    
    # rowData = spider._getRowData('http://www.shandong.gov.cn/art/2022/7/27/art_266672_1671.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    # print(len(urls))
    
    spider.scrapeAllProjectDataByPage(1, 1)
