from NMGGovSpider.NeiMengGuGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['NeiMengGuOthers']
    
    spider = NeimengguGovSpider(col)
    
    rowData = spider._getRowData('https://www.nmg.gov.cn/zwgk/zfxxgk/zc/qtwj/202102/t20210219_970476.html')
    data = spider._extractData(rowData)
    print(data)
    
    # urls = spider._getProjectID(76)
    # print(len(urls))
    # print(urls)
    
    # spider.scrapeAllProjectDataByPage(1, 202)
