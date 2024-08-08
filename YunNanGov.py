from YNGovSpider.YunNanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['云南省_政策文件汇总']
    
    spider = YunNanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.yn.gov.cn/zwgk/zcwj/zxwj/200804/t20080423_142742.html')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 209)
