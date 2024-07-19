from HLJGovSpider.HeiLongJiangGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['黑龙江_其他文件汇总']
    
    spider = HeilongjiangGovSpider(col)
    
    # rowData = spider._getRowData('https://www.hlj.gov.cn/hlj/c108372/202306/c00_31645049.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    

    spider.scrapeAllProjectDataByPage(1, 156)
