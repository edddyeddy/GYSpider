from XiamenGovSpider.xiamenGovSpider import *
from bs4 import BeautifulSoup

class xiamenCityHallSpider(XiamenGovSpider):
  def _getProjectID(self, pageNum) -> list:
      reuslt = list()
      pageIndex = "" if pageNum == 1 else "_{}".format(pageNum - 1)
      fileBaseUrl = 'https://www.xm.gov.cn/zwgk/flfg/sfwj'
      url = 'https://www.xm.gov.cn/zwgk/flfg/sfwj/index{}.htm'.format(pageIndex)
      rowData = requests.get(url).text
    
      
      soup = BeautifulSoup(rowData,'lxml')
      fileSoup = soup.find(attrs={"class":"gl_list1"})
      items = fileSoup.find_all(attrs={"target":"_blank"})
      for item in items:
          herf = item['href'][1:]
          link = fileBaseUrl + herf
          reuslt.append(link)
          
      return reuslt