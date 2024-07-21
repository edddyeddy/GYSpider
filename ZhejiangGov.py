from ZJGGovSpider.ZheJiangGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['浙江省_规章']
    
    spider = ZhejiangGovSpider(col)
    
    # rowData = spider._getRowData('https://www.zj.gov.cn/art/2024/2/1/art_1229604638_2512021.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 17)
