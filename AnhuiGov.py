from AHGovSpider.AnHuiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['安徽省_政策法规']
    
    spider = AnHuiGovSpider(col)
    
    # rowData = spider._getRowData('https://www.ah.gov.cn/public/1681/565333291.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 77)
