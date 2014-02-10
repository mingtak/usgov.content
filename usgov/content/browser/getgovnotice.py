# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Products.Five.browser import BrowserView
import urllib2
from ..config import GOV_NOTICE_URL
from ..config import PP
from ..config import FBO_INDEX
from ..config import TEST_STRING
from ..config import NOTICE_PACKAGES_PATH
from ..config import NOTICE_PACKAGES_URL
from ..config import ERROR_LOG_PATH
from plone import api
from random import random, choice, randrange
from datetime import datetime

def writeLog(logFilePath, log):
    with open(logFilePath, 'a') as logFile:
        logFile.write(log+'\n')
    return

class GetGovNotice(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        catalog = api.portal.get_tool(name='portal_catalog')
        page = int(1)
        hrefAndDate = list()
        breakOut = False
        while True:
            #取得公告列表
            try:
                getHtml = urllib2.urlopen(GOV_NOTICE_URL + str(page))
            except:
                writeLog(ERROR_LOG_PATH, str('%s\tweb site NO Response' % datetime.now()))
                if page == 1:
                    pass
                else:
                    continue
                raise IOError('web site NO Response')

            getNoticeHtmlDoc = getHtml.read()
            noticeListSoup = BeautifulSoup(getNoticeHtmlDoc)
            if page == 1:
                todayString = noticeListSoup.find(id='row_0').findAll('td')[-1].contents[0].strip().encode('utf-8')
                today = datetime.strptime(todayString, '%b %d, %Y')
            for i in range(PP):
                idAttr = 'row_%s' % str(i)
                trTag = noticeListSoup.find(id=idAttr)
                noticeHref = trTag.a['href']
                noticeDateString = trTag.findAll('td')[-1].contents[0].strip().encode('utf-8')
                noticeDate = datetime.strptime(noticeDateString, '%b %d, %Y')
                if noticeDate != today:
                    breakOut = True
                    break
                hrefAndDate.append(['%s%s' % (FBO_INDEX, noticeHref), noticeDate])
            if breakOut == True:
                break
            page += 1

        #依連結取得各頁面
        getResultsList = list()
        for link in hrefAndDate:
            # 比對 link,或已存在catalog，continue
            if len(catalog({'portal_type':'usgov.content.govnotice', 'noticeUrl':link[0]})) > 0:
                continue

            try:
                getNoticeHtml = urllib2.urlopen(link[0])
            except:
                continue
            doc = getNoticeHtml.read()
            soup = BeautifulSoup(doc)
            try:
                #案名
                noticeTitle = soup.body.h2.contents[0].strip().encode('utf-8')
                #案號
                solicitationNumber = soup(id='dnf_class_values_procurement_notice__solicitation_number__widget')[0].contents[0].strip().encode('utf-8')
                #標案型態
                noticeType = soup(id='dnf_class_values_procurement_notice__procurement_type__widget')[0].contents[0].strip().encode('utf-8')
                #簡述
                synopsis = soup(id='dnf_class_values_procurement_notice__description__widget')
                synopsis = str() if synopsis == [] else str(synopsis[0]).replace(NOTICE_PACKAGES_PATH, NOTICE_PACKAGES_URL)
                #附檔
                noticePackages = soup(id='so_formfield_dnf_class_values_procurement_notice__packages__0__files_')
                noticePackages = str() if noticePackages == [] else str(noticePackages[0]).replace(NOTICE_PACKAGES_PATH, NOTICE_PACKAGES_URL)
                #承辦地址
                contractingOfficeAddress = soup(id='dnf_class_values_procurement_notice__office_address_text__widget')
                contractingOfficeAddress = str() if contractingOfficeAddress == [] else contractingOfficeAddress[0].contents[0].strip().encode('utf-8')
                #履約地址
                placeOfPerformance = soup(id='dnf_class_values_procurement_notice__place_of_performance_text__widget')
                placeOfPerformance = str() if placeOfPerformance == [] else placeOfPerformance[0].contents[0].strip().encode('utf-8')
                #承辦人
                primaryPointOfContact = soup(id='dnf_class_values_procurement_notice__primary_poc__widget')
                primaryPointOfContact = str() if primaryPointOfContact == [] else primaryPointOfContact[0].contents[0].strip().encode('utf-8')
                #代理人
                secondaryPointOfContact = soup(id='dnf_class_values_procurement_notice__secondary_poc__widget')
                secondaryPointOfContact = str() if secondaryPointOfContact == [] else secondaryPointOfContact[0].contents[0].strip().encode('utf-8')
                #附加資訊
                additionalInfo = soup(id='dnf_class_values_procurement_notice__additional_info_link__widget')
                additionalInfo = str() if additionalInfo == [] else additionalInfo[0].contents[0].strip().encode('utf-8')
                #聯絡地點
                pointOfContacts = soup(id='dnf_class_values_procurement_notice__poc_text__widget')
                pointOfContacts = str() if pointOfContacts == [] else pointOfContacts[0].contents[0].strip().encode('utf-8')
                #公告日期
                postedDate = link[1]
                #連結網址
                noticeUrl = link[0]

                getResultsList.append({'noticeTitle':noticeTitle,
                                       'solicitationNumber':solicitationNumber,
                                       'noticeType':noticeType,
                                       'synopsis':synopsis,
                                       'noticePackages':noticePackages,
                                       'contractingOfficeAddress':contractingOfficeAddress,
                                       'placeOfPerformance':placeOfPerformance,
                                       'primaryPointOfContact':primaryPointOfContact,
                                       'secondaryPointOfContact':secondaryPointOfContact,
                                       'additionalInfo':additionalInfo,
                                       'pointOfContacts':pointOfContacts,
                                       'postedDate':postedDate,
                                       'noticeUrl':noticeUrl})
            except:
                writeLog(ERROR_LOG_PATH, str('%s\t%s' % (datetime.now(),link)))
                pass
        add_count = 0
        for result in getResultsList:
            if len(catalog({'portal_type':'usgov.content.govnotice', 'noticeUrl':result['noticeUrl']})) > 0:
                continue
            else:
                try:
                    contentId = '%s%s' % (str(datetime.now().strftime('%Y%m%d%H%M')), str(randrange(10000000,100000000)))
                    api.content.create(container=portal['notice'],
                                       type='usgov.content.govnotice',
                                       title=result['noticeTitle'],
                                       id=contentId,
                                       solicitationNumber = result['solicitationNumber'],
                                       noticeType = result['noticeType'],
                                       synopsis = result['synopsis'],
                                       noticePackages = result['noticePackages'],
                                       contractingOfficeAddress = result['contractingOfficeAddress'],
                                       placeOfPerformance = result['placeOfPerformance'],
                                       primaryPointOfContact = result['primaryPointOfContact'],
                                       additionalInfo = result['additionalInfo'],
                                       pointOfContacts = result['pointOfContacts'],
                                       postedDate = result['postedDate'],
                                       noticeUrl = result['noticeUrl'],)
                except:
                    continue
                objectBrain = catalog(id=contentId)
                object = objectBrain[0].getObject()
                object.reindexObject()
                add_count += 1
        return '總共新增 %s 筆,現在的page = %s' % (add_count, page)
