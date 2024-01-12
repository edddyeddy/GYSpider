from XiamenGovSpider.xiamenGovSpider import *
from bs4 import BeautifulSoup

class xiamenDepartmentSpider(XiamenGovSpider):
  def _getProjectID(self, pageNum) -> list:
      reuslt = list()
      pageIndex = "" if pageNum == 1 else "_{}".format(pageNum - 1)
      fileBaseUrl = 'https://www.xm.gov.cn/zwgk/flfg/bmwj/'
      url = 'https://www.xm.gov.cn/zwgk/flfg/bmwj/index{}.htm'.format(pageIndex)
      rowData = requests.get(url).text
    
      
      soup = BeautifulSoup(rowData,'lxml')
      fileSoup = soup.find(attrs={"class":"gl_list1"})
      items = fileSoup.find_all(attrs={"target":"_blank"})
      for item in items:
          herf = item['href']
          reuslt.append(herf)
          
      return reuslt