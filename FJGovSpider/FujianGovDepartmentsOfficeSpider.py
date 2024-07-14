from FJGovSpider.FuJianGovSpider import *


class FujianGovDepartmentsOfficeSpider(FuJianGovSpider):
    """
    福建省办公厅行政规范文件
    """

    def _getProjectID(self, pageNum=None) -> list:
        _headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'Secure; JSESSIONID=F97D92332ECBD3EAC692E785D7702A27; _gscu_1267028586=20235983jxy3vm14; _gscbrs_1267028586=1; BFreeDialect=0; BFreeTip=1; Secure; _gscs_1267028586=t202422828y14pr15|pv:4',
            'DNT': '1',
            'Referer': 'https://www.fujian.gov.cn/zwgk/zfxxgk/szfwj/jgzz/xzgfxwj/szf.htm',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }


        url = 'https://www.fujian.gov.cn/was5/web/search?channelid=291575&templet=docs.jsp&sortfield=-pubdate&classsql=chnlid%3D58154*puborg%3D%27%E7%A6%8F%E5%BB%BA%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C%27&prepage=15&page={}'.format(
            pageNum)

        urls = list()
        row_data = self._getJSONData(url, _headers)
        for item in row_data['docs']:
            url = item['url']
            if(url.startswith('http')):
                urls.append(url)
        return urls

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID

        row_page = requests.get(url)
        row_page.encoding = 'utf-8'
        rowData = {
            'url': projectID,
            'rowPage': row_page.text
        }
        return rowData
