from XiamenGovSpider.xiamenCityHallSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['XiamenCityHall']
    
    spider = xiamenCityHallSpider(col)
    # rowData = spider._getRowData('https://www.xm.gov.cn/zwgk/flfg/sfwj/202311/t20231110_2797432.htm')
    # data = spider._extractData(rowData)
    # print(data)
    
    spider.scrapeAllProjectDataByPage(1,50)