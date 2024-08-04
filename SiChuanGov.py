from SCGovSpider.SiChuanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['四川省_川办函']
    
    spider = SichuanGovSpider(col)
    
    # rowData = spider._getRowData('http://www.sc.gov.cn/10462/10464/10684/10693/2015/5/4/10334615.shtml', '2024/02/22 17:47:44')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 47)
