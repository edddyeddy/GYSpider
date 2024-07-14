from FJGovSpider.FuJianGovSpider import *


class FujianGovFile(FuJianGovSpider):
    """
    福建省政府文件
    """

    def _getProjectID(self, pageNum=None) -> list:
        _headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'Secure; JSESSIONID=66B1C0C24F8BBC2330F4AD0DE6EB4719; _gscu_1267028586=20235983jxy3vm14; _gscbrs_1267028586=1; BFreeDialect=0; BFreeTip=1; Secure; _gscs_1267028586=t202453327sexnm23|pv:11',
            'DNT': '1',
            'Referer': 'https://www.fujian.gov.cn/zwgk/zfxxgk/szfwj/?type=3',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        _params = {
            'channelid': '291575',
            'templet': 'docs.jsp',
            'sortfield': '-pubdate',
            # 'classsql': '''(fileno=%闽政〔%*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            # 'classsql': '''(fileno=%福建省人民政府令%,%省政府令%*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            # 'classsql': '''(fileno=%闽政文%*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            # 'classsql':'''(fileno=%闽政办〔%*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            # 'classsql':'''(fileno=%闽政办函%*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            'classsql':'''(fileno!=(%福建省人民政府令%,%省政府令%,%闽政〔%,%闽政文%,%闽政办〔%,%闽政办函%)*docpuburl='%/zwgk/zfxxgk/szfwj/%'*modal=1*chnlid!=58154*chnlid!=60180*chnlid!=60181*chnlid!=60182)''',
            'prepage': '10',
        }

        url = 'https://www.fujian.gov.cn/was5/web/search?'.format(
            pageNum)

        urls = list()
        _params['page'] = pageNum
        row_data = self._getJSONData(url, _headers, _params)
        for item in row_data['docs']:
            url = item['url']
            if (url.startswith('http')):
                urls.append(url)
        # print(len(urls))
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
