from bs4 import BeautifulSoup
import time
import re


class SinaExtractor(object):
    """
    从新浪微公益原始信息中提取需要的数据
    """


    def getProjectInfo(self,projectID,rowData):
        """
        获取项目具体信息以及项目进展
        args:
            id(int):项目id
        return
            info(dict):项目具体信息
            progress(list):项目进展信息
        """
        ret = {
            'projectID': projectID,
            'title': None,
            'cate': None,
            'intro': None,
            'needMoney': None,
            'donateNum': None,
            'receivedMoney': None,
            'desc': None,
            'sponsor': {
                'name':None,
                'weibo':None
            },
            'receiver': {
                'name':None,
                'weibo':None
            },
            'descLength':None,
            'imageNumber':None,
            'projectTime': None,
            'feedBackCnt' : None,
            'getTime': time.time()
        }
        soup = BeautifulSoup(rowData, 'lxml')

        # 获取标题
        ret['title'] = soup.find(class_="tit").string
        # 获取类别
        ret['cate'] = soup.find(class_="tagging_a").string
        # 获取简介
        ret['intro'] = soup.find(class_="txt").string
        # 获取捐赠信息
        ret['needMoney'] = soup.find(class_='num-right').dd.string
        ret['donateNum'] = soup.find(class_='num-center').dd.string
        ret['receivedMoney'] = soup.find(class_='num-left').dd.string
        # 获取描述信息
        descInfo = soup.find(id='help_info_1')
        ret['desc'] = descInfo.text.strip()
        ret['descLength'] = len(ret['desc'])
        # 获取图片数量
        ret['imageNumber'] = len(descInfo.find_all('img'))
        # 获取机构信息
        infoList = soup.find(class_='tab_b_con').find_all(
            class_='clearfix')
        ret['sponsor']['name'] = infoList[1].find('h5').text
        ret['sponsor']['weibo'] = infoList[1].find('a').get('href')
        ret['receiver']['name'] = infoList[2].find('h5').text
        ret['receiver']['weibo'] = infoList[2].find('a').get('href')
        # 获取项目时间
        help_info = soup.find(id='help_info')
        ret['projectTime'] = re.search(
            r'\d{4}.\d{2}.\d{2}-\d{4}.\d{2}.\d{2}', help_info.text).group()
        # 获取反馈信息数量
        infos = soup.find_all(class_='tab_progress_list clearfix')
        ret['feedBackCnt'] = len(infos)

        return ret

