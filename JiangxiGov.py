from JXGovSpider.JiangxiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['江西省_赣府厅发']
    
    spider = JiangxiGovSpider(col)
    
    # rowData = spider._getRowData('https://www.jiangxi.gov.cn/art/2022/7/18/art_4975_4032897.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 142)
