from JSGovSpider.JiangSuGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    jiangsuGov = db['JiangsuGovPolicy']

    spider = JiangSuGovSpider(jiangsuGov)

    # rowData = spider._getRowData('http://www.jiangsu.gov.cn/art/2013/11/3/art_46143_2543964.html')
    # data = spider._extractData(rowData)
    # print(data)

    # urls = spider._getProjectID(1)
    # urls = spider._saveProjectIDPeriodically(1000)
    # print(urls)

    # spider.updateProjectDataPeriodically(1000000)
    spider._extractProjectDataPeriodically(100000)

    # spider.scrapeAllProjectDataByPage(1, 236)
