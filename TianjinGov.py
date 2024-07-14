from TJGovSpider.TianJinGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    TianJinGov = db['天津市_汇总']
    
    spider = TianJinGovSpider(TianJinGov)
    
    # rowData = spider._getRowData('https://www.tj.gov.cn/zwgk/szfwj/tjsrmzf/202303/t20230320_6143854.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    # spider.updateProjectDataPeriodically(1000000)
    # spider._extractProjectDataPeriodically(100000)
    
    spider.scrapeAllProjectDataByPage(1, 67)
