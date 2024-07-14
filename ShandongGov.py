from ShandongGovSpider.ShanDongGovSpider import *
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["GYDatabase"]
    ShandongGov = db['山东省_行政规范文件汇总']
    
    spider = ShandongGovSpider(ShandongGov)
    
    # rowData = spider._getRowData('http://www.shandong.gov.cn/jpaas-jpolicy-web-server/front/info/detail?iid=72f3842f52414d3282318b62e965126f',{'projectID': 'http://www.shandong.gov.cn/jpaas-jpolicy-web-server/front/info/detail?iid=72f3842f52414d3282318b62e965126f', 'rowData': {'publishDate': '2024-05-24', 'title': '山东省人民政府关于2023年度县域经济高质量发展差异化评价结果的通报'}})
    # data = spider._extractData(rowData)
    # print(data)
    
    # urls = spider._getProjectID(1)
    # print(urls)
    
    spider.scrapeAllProjectDataByPage(1, 76)
