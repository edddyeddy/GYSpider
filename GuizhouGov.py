from GZGovSpider.GuiZhouGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['贵州省_失效废止文件']
    
    spider = GuiZhouGovSpider(col)
    
    # rowData = spider._getRowData('https://www.guizhou.gov.cn/zwgk/zcfg/szfwj/szfl/202201/t20220114_72313231.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 26)
