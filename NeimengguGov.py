from NMGGovSpider.NeiMengGuGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['内蒙古_政府文件']
    
    spider = NeimengguGovSpider(col)
    
    # rowData = spider._getRowData('http://www.dwq.gov.cn//dwq/zwgk/zfxxgkzl/fdzdgknr/xzgfxwj/nmylysl/2024051410154595953/index.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 145)
