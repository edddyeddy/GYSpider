from HBGovSpider.hebeiGovOfficeNormativeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    hebeiGovOfficeNormativeCol = db['河北_行政规范_省政府办公厅']
    
    spider = hebeiGovOfficeNormativeSpider(hebeiGovOfficeNormativeCol)
    
    # rowData = spider._getRowData('https://www.hebei.gov.cn/columns/3d33a20b-4271-4b3b-8cae-3664e980d262/202307/21/fbdc00e3-4f8b-11ee-beb8-6018954d7f6f.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 15)
