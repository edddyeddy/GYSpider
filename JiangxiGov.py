from JXGovSpider.JiangxiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['江西省_省政府办公厅']
    
    spider = JiangxiGovSpider(col)
    
    # rowData = spider._getRowData('https://www.jiangxi.gov.cn/art/2024/7/25/art_5057_4963506.html?xxgkhide=1')
    # data = spider._extractData(rowData)
    # print(data)
    
    urls = spider._getProjectID(142)
    print(len(urls))
    print(urls)
    
    # spider.scrapeAllProjectDataByPage(1, 21)
