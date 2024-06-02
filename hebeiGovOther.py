from HBGovSpider.hebeiGovOtherSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    hebeiGovOtherCol = db['河北省_其他文件_省政府']
    
    spider = hebeiGovOtherSpider(hebeiGovOtherCol)
    
    # rowData = spider._getRowData('https://www.hebei.gov.cn/columns/84f73ef0-6a8d-495e-9bf2-acffc68c31f6/202402/22/afa99eb4-c896-430f-a81b-6cce6cfcafed.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 26)
