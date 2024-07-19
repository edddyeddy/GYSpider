from HBGovSpider.hebeiGovOfficeOtherSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    hebeiGovOfficeOtherCol = db['河北省_其他文件_政府办']
    
    spider = hebeiGovOfficeOtherSpider(hebeiGovOfficeOtherCol)
    
    rowData = spider._getRowData('https://www.hebei.gov.cn/columns/8dff597e-a95c-4b20-b321-a5320af40141/202405/15/39e53640-1494-4c39-9d42-203cee04982d.html')
    print(rowData)
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 30)
