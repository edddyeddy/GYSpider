from SXGovSpider.ShanXiGovNormativeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    shanxiGov = db['山西省_行政规范文件_其他部门']
    
    spider = ShanxiGovNormativeSpider(shanxiGov)
    
    # rowData = spider._getRowData('https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/fdzdgknr/lzyj/szfl/202205/t20220513_5978858_gzk.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    # spider.scrapeAllProjectDataByPage(1, 1)
    # spider._saveProjectIDPeriodically(100000)
    # def isFinished(rowData):
    #     return True
    # spider._updateProjectDataPeriodically(isFinished, 10000)
    spider._extractProjectDataPeriodically(100000)
