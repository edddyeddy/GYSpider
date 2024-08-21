from QHGovSpider.QinghaiGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['青海省_青政办函']
    
    spider = QinghaiGovSpider(col)
    
    # rowData = spider._getRowData('http://www.qinghai.gov.cn/xxgk/xxgk/fd/lzyj/gfxwj/szf/201712/t20171222_18026.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)

    spider.scrapeAllProjectDataByPage(1, 8)
