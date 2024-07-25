from HNGovSpider.HainanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['海南省_其他文件']
    
    spider = HainanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.hainan.gov.cn/hainan/szfwj/202404/854d61402bfd4970b8bb96c6f9113efa.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 9)
