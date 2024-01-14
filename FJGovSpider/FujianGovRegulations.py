from FJGovSpider.FuJianGovSpider import *
class FujianGovRegulationsSpider(FuJianGovSpider):
    
    def _getProjectID(self, pageNum = None) -> list:
        _headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': '_gscu_1267028586=051550931vvsol11; BFreeTip=1; _gscbrs_1267028586=1; BFreeDialect=0; _gscs_1267028586=0520913562pj5b96|pv:2; Secure',
            'DNT': '1',
            'Pragma': 'no-cache',
            'Referer': 'https://www.fujian.gov.cn/zwgk/zfxxgk/zfxxgkzc/fjsgzk/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        _params = {
            'channelid': '516770',
            'templet': 'docs.jsp',
            'sortfield': '-docorder',
            'classsql': 'chnlid=54310',
            'prepage': '501',
            'page': '1',
        }
        
        url = 'https://www.fujian.gov.cn/fjdzapp/search'
        urls = list()
        row_data = self._getJSONData(url, _headers, _params)
        
        for doc in row_data['docs']:
            urls.append(doc['chnldocurl'])
        return urls

    def _getRowData(self, projectID, rowData = None) -> dict:
        url = projectID
        
        row_page = requests.get(url)
        row_page.encoding = 'utf-8'
        rowData = {
            'url': projectID,
            'rowPage': row_page.text
        }
        return rowData