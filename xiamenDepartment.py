from XiamenGovSpider.xiamenDepartmentSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['XiamenDepartment']
    
    spider = xiamenDepartmentSpider(col)
    
    rowData = spider._getRowData('http://ga.xm.gov.cn/zwgk/zfxxgkzl/gkml/zcfg/gfxwj/202304/t20230406_2750015.htm')
    data = spider._extractData(rowData)
    print(data)
    
    # pageLinks = spider._getProjectID(1)
    # print(pageLinks)
    
    # spider.scrapeAllProjectDataByPage(1,25)