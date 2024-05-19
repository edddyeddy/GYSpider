from Spider.Spider import *
import requests
from SXGovSpider.ShanXiGovExtractor import *
import re
from urllib.parse import urljoin
import time


class ShanxiGovNormativeSpider(Spider):
    """
    抓取山西省人民政府数据
    """
    
    dept_urls = [
        # {'orgName': '山西省人民政府', 'href': '../srmzf/'},
        {'orgName': '山西省人民政府办公厅', 'href': '../srmzfbgt/'},
        # {'orgName': '山西省发展和改革委员会', 'href': '../sfzhggwyh_76476/'},
        # {'orgName': '山西省教育厅', 'href': '../sjyt_76477/'},
        # {'orgName': '山西省科学技术厅', 'href': '../skxjst_76478/'},
        # {'orgName': '山西省工业和信息化厅', 'href': '../sgyhxxht_76479/'},
        # {'orgName': '山西省公安厅', 'href': '../sgat_76480/'},
        # {'orgName': '山西省民政厅', 'href': '../smzt_76481/'},
        # {'orgName': '山西省司法厅', 'href': '../ssft_76482/'},
        # {'orgName': '山西省财政厅', 'href': '../sczt_76483/'},
        # {'orgName': '山西省人力资源和社会保障厅', 'href': '../srlzyhshbzt_76484/'},
        # {'orgName': '山西省自然资源厅', 'href': '../szrzyt_76485/'},
        # {'orgName': '山西省生态环境厅', 'href': '../ssthjt_76486/'},
        # {'orgName': '山西省住房和城乡建设厅', 'href': '../szfhcxjst_76487/'},
        # {'orgName': '山西省交通运输厅', 'href': '../sjtyst_76488/'},
        # {'orgName': '山西省水利厅', 'href': '../sslt_76489/'},
        # {'orgName': '山西省农业农村厅', 'href': '../snynct_76490/'},
        # {'orgName': '山西省商务厅', 'href': '../sswt_76491/'},
        # {'orgName': '山西省文化和旅游厅', 'href': '../swhhlyt_76492/'},
        # {'orgName': '山西省卫生健康委员会', 'href': '../swsjkwyh_76493/'},
        # {'orgName': '山西省退役军人事务厅', 'href': '../styjrswt_76494/'},
        # {'orgName': '山西省应急管理厅', 'href': '../syjglt_76495/'},
        # {'orgName': '山西省市场监督管理局', 'href': '../../szfzsjg_76500/sscjdglj_76501/'},
        # {'orgName': '山西省广播电视局', 'href': '../../szfzsjg_76500/sgbdsj_76502/'},
        # {'orgName': '山西省体育局', 'href': '../../szfzsjg_76500/styj_76503/'},
        # {'orgName': '山西省统计局', 'href': '../../szfzsjg_76500/stjj_76504/'},
        # {'orgName': '山西省行政审批服务管理局', 'href': '../../szfzsjg_76500/sxzspfwglj_76506/'},
        # {'orgName': '山西省地方金融监督管理局', 'href': '../../szfzsjg_76500/sdfjrjdglj_76508/'},
        # {'orgName': '山西省能源局', 'href': '../../szfzsjg_76500/snyj_76509/'},
        # {'orgName': '山西省文物局', 'href': '../../szfzsjg_76500/swwj_76510/'},
        # {'orgName': '山西省人民防空办公室', 'href': '../../szfzsjg_76500/srmfkbgs_76511/'},
        # {'orgName': '山西省乡村振兴局', 'href': '../../szfzsjg_76500/sxczxj_76512/'},
        # {'orgName': '山西省医疗保障局', 'href': '../../szfzsjg_76500/sylbzj_76513/'},
        # {'orgName': '山西省粮食和物资储备局', 'href': '../../szfbmgljg_76514/slshwzcbj_76515/'},
        # {'orgName': '山西省小企业发展促进局', 'href': '../../szfbmgljg_76514/sxqyfzcjj_76516/'},
        # {'orgName': '山西省林业和草原局', 'href': '../../szfbmgljg_76514/slyhcyj_76518/'},
        # {'orgName': '山西省药品监督管理局', 'href': '../../szfbmgljg_76514/sypjdglj_76519/'}
    ]


    def __init__(self, collection) -> None:
        self.collection = collection
        
    def __get_project_list_url(self, href, page_num):
        pageIndex = "_{}".format(page_num - 1) if page_num != 1 else ""
        base_url = 'https://www.shanxi.gov.cn/zfxxgk/zfxxgkzl/zc/xzgfxwj/bmgfxwj1/szfzcbm_76475/srmzf/'
        page_url = './index{}.shtml'.format(pageIndex)
        return urljoin(urljoin(base_url, href), page_url)

    def __get_project_urls(self, page_url):
        result = list()
        print(page_url)
        rowData = requests.get(page_url)
        rowData.encoding = 'utf-8'

        soup = BeautifulSoup(rowData.text, 'lxml')
        items = soup.find_all(
            attrs={"class": "sxinfo-pubfiles-item"})

        for item in items:
            link = item.find(
                'a', href=lambda href: href and href.endswith('.shtml'))
            result.append(urljoin(page_url, link['href']))
        return result

    def __get_project_list_page_num(self, url):
        rowData = requests.get(url)
        rowData.encoding = 'utf-8'
        text = rowData.text
        
        pattern = r'var countPage = (\d+)'
        match = re.search(pattern, text)
        count_page = match.group(1)
        return int(count_page)

    def _getProjectID(self, pageNum=None) -> list:
        result = list()
        for dept in self.dept_urls:
            print(dept['orgName'])
            first_page_url = self.__get_project_list_url(dept['href'], 1)
            page_num = self.__get_project_list_page_num(first_page_url)
            for i in range(1, page_num + 1):
                page_url = self.__get_project_list_url(dept['href'], i)
                project_urls = self.__get_project_urls(page_url)
                # print(project_urls)
                result += project_urls
                # time.sleep(5)
        return result

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
        extractor = ShanxiGovExtractor()
        return extractor.extractShanxiGovData(rowData)

    def _saveData(self, data) -> None:
        self.collection.insert_one(data)

    def _isExist(self, projectID) -> bool:
        return self.collection.find_one({'projectID': projectID}) != None
