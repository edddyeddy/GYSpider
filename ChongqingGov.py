from CQGovSpider.ChongQingGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['重庆市_其他文件']
    
    spider = ChongqingGovSpider(col)
    
    # rowData = spider._getRowData('https://www.cq.gov.cn/zwgk/zfxxgkml/szfwj/qtgw/202407/t20240709_13360299.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 67)
