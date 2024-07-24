from HNGovSpider.HainanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['海南省_行政规范性文件']
    
    spider = HainanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.hainan.gov.cn/hainan/flfgxzgfxwj/202405/6e4923fed21c47dfbfc2b346e5983210.shtml?ddtab=true')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 31)
