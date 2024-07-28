from HuNanGovSpider.HunanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['湖南省_省政府办公厅文件']
    
    spider = HunanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.hunan.gov.cn/hnszf/xxgk/wjk/szfwj/200907/t20090713_4824371.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 34)
