from JLGovSpider.JiLinGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['吉林省_吉政办明电']
    
    spider = JilinGovSpider(col)
    
    # rowData = spider._getRowData('https://www.ln.gov.cn/web/zwgkx/zfwj/bmwj/ssft/BEA1819B1A314E60A7B5A2EFC3C22995/index.shtml')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 22)
