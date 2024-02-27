from SXGovSpider.ShanXiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    shanxiGov = db['ShanXiRegulations']
    
    spider = ShanxiGovSpider(shanxiGov)
    
    # rowData = spider._getRowData('https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/fdzdgknr/lzyj/szfl/202205/t20220513_5978858_gzk.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 6)
