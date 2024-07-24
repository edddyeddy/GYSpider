from Spider.Spider import *
import requests
from HuBeiGovSpider.HubeiGovExtractor import *
from bs4 import BeautifulSoup
import urllib
import time
import re


class HubeiGovSpider(Spider):
    """
    抓取湖北人民政府数据
    """
    def __init__(self, collection) -> None:
        self.collection = collection
        self._cookies = {
            '97badf5c34b18827e4': 'a6b1225bafc57145a1e2d20d9a2b3e68',
            '_trs_uv': 'lyzxsmrx_3027_94y7',
            '_trs_ua_s_1': 'lyzxsmrx_3027_3end',
            '924omrTVcFchP': '0fOfxfNngfW7M8DLk9q.Khu3rByVDixJoYsBgL76Sb0JZRpZ9KsgFVCB6el3zLTbv.BD00jqcouSyG9cIR3yML6hJcTPqG6CSrcIyiD5fkzNE_imQJ6FQJWxb4BtnS2CxvFSyzXjp8zgti6MdybMyTzufs2887sHzvUZfisLaXL2chWr4nHj8G1HTRGpKhI7PEXU4etV.gRPR.c2mefWUuleyEjzDTbIAeXMao9ZjGFBYwV4yKb0CI5rvkw.ZUrr7nspyfJKdn261GR1fnWWg3taTVErOynumKc5HXIiLZqPAHSgcKCVXPOk9N.IpDwh_Sv8w0KqI_ESfQLh6SphutGm4td6PXVSaidmrQKIHQeE',
        }

        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': '97badf5c34b18827e4=a6b1225bafc57145a1e2d20d9a2b3e68; _trs_uv=lyzxsmrx_3027_94y7; _trs_ua_s_1=lyzxsmrx_3027_3end; 924omrTVcFchP=0fOfxfNngfW7M8DLk9q.Khu3rByVDixJoYsBgL76Sb0JZRpZ9KsgFVCB6el3zLTbv.BD00jqcouSyG9cIR3yML6hJcTPqG6CSrcIyiD5fkzNE_imQJ6FQJWxb4BtnS2CxvFSyzXjp8zgti6MdybMyTzufs2887sHzvUZfisLaXL2chWr4nHj8G1HTRGpKhI7PEXU4etV.gRPR.c2mefWUuleyEjzDTbIAeXMao9ZjGFBYwV4yKb0CI5rvkw.ZUrr7nspyfJKdn261GR1fnWWg3taTVErOynumKc5HXIiLZqPAHSgcKCVXPOk9N.IpDwh_Sv8w0KqI_ESfQLh6SphutGm4td6PXVSaidmrQKIHQeE',
            'DNT': '1',
            'Referer': 'https://www.hubei.gov.cn/xxgk/gz/index.shtml',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def _getProjectID(self, pageNum=None) -> list:
        results = set()
        pageIndex = "_{}".format(pageNum - 1) if pageNum != 1 else ""
        url = f'https://www.hubei.gov.cn/xxgk/gz/index{pageIndex}.shtml'
        resp = requests.get(url, headers=self._headers, cookies=self._cookies)
        # resp.encoding = 'utf-8'
        print(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        print(soup)
        for item in soup.find_all(attrs={"target": "_blank"}, title=True):
            complete_link = urllib.parse.urljoin(url, item['href'])
            results.add(complete_link)

        return results

    def _getRowData(self, projectID, rowData=None) -> dict:
        url = projectID
        rowPage = requests.get(url)
        rowPage.encoding = 'utf-8'
        rowData = {
            'projectID': projectID,
            'rowPage': rowPage.text
        }
        return rowData

    def _extractData(self, rowData) -> dict:
        extractor = HubeiGovExtractor()
        return extractor.extractHubeiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
