from XiamenGovSpider.xiamenCityHallOfficeSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['XiamenCityHallOffice']
    
    spider = xiamenCityHallOfficeSpider(col)
    # rowData = spider._getRowData('https://www.xm.gov.cn/zwgk/flfg/sfbwj/202303/t20230306_2723191.htm')
    # data = spider._extractData(rowData)
    # print(data)
    
    # pageLinks = spider._getProjectID(2)
    # print(pageLinks)
    
    spider.scrapeAllProjectDataByPage(1,50)