from bs4 import BeautifulSoup
import requests
import json
import hashlib
from datetime import datetime, date, timedelta
import time
import datetime
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    'Referer':'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'
}
datas = {
    'page.currentPage':'1',
    'page.perPageSize':'20',
    'noticeBean.sourceCH':'',
    'noticeBean.source':'',
    'noticeBean.title':'', #山西移动
    'noticeBean.startDate':'',
    'noticeBean.endDate':''
}
dict_data={}
dict_tmp={}
break_tag=0
for i in range(1,20):
    fin_date_tmp=(date.today() + timedelta(days = -1)).timetuple()
    fin_date=str(fin_date_tmp.tm_year) + '-' + str(fin_date_tmp.tm_mon) + '-' + str(fin_date_tmp.tm_mday)
    if break_tag==1:
        break
    datas['page.currentPage'] = i
    r=requests.post('https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2',  headers=headers, data=datas).content
    s=r.decode('utf-8').rstrip()
    tb=BeautifulSoup(s, 'html.parser').find('table', class_='zb_result_table')
    for i in tb.find_all('tr', attrs={"onmousemove": "cursorOver(this)"}):
        tds = i.find_all('td')
        time1=time.strptime(tds[3].get_text(),'%Y-%m-%d')
        time2=time.strptime(fin_date,'%Y-%m-%d')
        if time1<time2:
            break_tag = 1
            break
        if dict_data.get((i.attrs['onclick'][14:-2]),'Notexist')!='Notexist':
            break_tag = 1
            break
        dict_tmp[tds[0].get_text()] = 'comp'
        dict_tmp[tds[1].get_text()] = 'type'
        dict_tmp[tds[3].get_text()] = 'date'
        if 'title' in tds[2].a.attrs:
            dict_tmp[tds[2].a.attrs['title']] = 'title'
        else:
            dict_tmp[tds[2].get_text().strip()] = 'title'
        dict_new = dict(zip(dict_tmp.values(), dict_tmp.keys()))
        dict_tmp={}
        dict_data[(i.attrs['onclick'][14:-2])] = dict_new