from HenanGovSpider.henanGovOtherSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    HenanGovOtherCol = db['河南省_其他']
    
    spider = henanGovOtherSpider(HenanGovOtherCol)
    
    # rowData = spider._getRowData('http://www.gd.gov.cn/gkmlpt/content/4/4284/post_4284753.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 3)
