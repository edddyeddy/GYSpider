from HNGovSpider.HainanGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    col = db['海南省_省政府办公厅']
    
    spider = HainanGovSpider(col)
    
    # rowData = spider._getRowData('https://www.hainan.gov.cn/hainan/fzfztz/202301/dd4d9016cf114d11a5d14564b70f99e0.shtml?ddtab=true')
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(len(urls))
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 135)
