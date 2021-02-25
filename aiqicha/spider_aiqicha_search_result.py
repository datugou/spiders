import re,json,time
import requests
from bs4 import BeautifulSoup

def get_proxy():
    # 需要根据自己ip代理服务构造一个函数
    # 返回一个ip地址
    # 格式"http://000.000.000.000:0000"
    return line

def req_get_proxy(url):
    global line
   
    # 代理不可用则直接换一个代理ip
    try:
        proxy = {
            'http':line,
            'https':line
        }
        resp = requests.get(url, headers = headers, timeout=10)
    except:
        line = get_proxy()
        resp = req_get(url)
    
    # 服务器禁用该代理ip，则再换一个
    if 'check' in resp.url:
        line = get_proxy()
        resp = req_get(url)
        
    return resp

t0 = time.time()
def req_get(url):
    # 每次禁用ip，1min后会解封
    global t0
    try:
        resp = requests.get(url, headers = headers, timeout=10)
    except:
        resp = req_get(url)
    if 'check' in resp.url:
        t1 = time.time()
        dt = 60-t1+t0
        dtt = dt if dt >= 0 else 0
        time.sleep(dtt)
        resp = req_get(url)
        t0 = time.time()
    return resp

def write_comp(resp):
    # 直接存json格式
    page_data = re.findall('pageData = ({.*})',resp.text)[0]
    jd = json.loads(page_data)
    for comp in jd['result']['resultList']:
        asp = json.dumps(comp)
        out_file.write(asp+'\n')
        

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
provs = [110000,120000,130000,140000,150000,210000,220000,230000,310000,320000,330000,340000,350000,360000,370000,410000,420000,430000,440000,450000,460000,500000,510000,520000,530000,540000,610000,620000,630000,640000,650000]
rcl = [1,2,3,4,5]
sy = ['1990-2005','2005-2010','2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2015-2016','2016-2017','2017-2018','2018-2019','2019-2020','2020-2021','2021-2022']
wdl = 'ABCDEFGHIJKLMNOPQRST'


# 有代理池的把use_proxy的值改成1
use_proxy = 0
kw = '填写需要的搜索词'
out_file = open(r'D:\data.txt','a')
out_range = []


if use_proxy == 1:
    line = get_proxy()
    req_get = req_get_proxy
for pr in provs:
    for lv in rcl:
        for ar in list(wdl):
            url0 = 'https://aiqicha.baidu.com/s?q=%s&f={"provinceCode":"%d","regCapLevel":"level%d","industryCode1":"%s"}'%(kw,pr,lv,ar)
            resp = req_get(url0)
            
            page_data = re.findall('pageData = ({.*})',resp.text)[0]
            jd = json.loads(page_data)
            tnum = int(jd['result']['totalNumFound'])
            print(pr,lv,ar,tnum)
            
            if tnum <= 1000:
                page = tnum//10 + 1
                for p in range(page):
                    try:
                        resp = req_get(url0 + '&p=%d'%(p+1))
                        write_comp(resp)
                    except:
                        line = get_proxy()
                        resp = req_get(url0 + '&p=%d'%(p+1))
                        write_comp(resp)
            # 大于1000条，进行拆分检索
            elif tnum > 1000:
                for yr in sy:
                    url = 'https://aiqicha.baidu.com/s?q=%s&f={"provinceCode":"%d","regCapLevel":"level%d","industryCode1":"%s","startYear":"%s"}'%(kw,pr,lv,ar,yr)
                    try:
                        resp = req_get(url)
                        write_comp(resp)
                    except:
                        line = get_proxy()
                        resp = req_get(url)
                        write_comp(resp)

                    page_data = re.findall('pageData = ({.*})',resp.text)[0]
                    jd = json.loads(page_data)
                    tnum = int(jd['result']['totalNumFound'])
                    print(tnum, ar)
                    if tnum//10 > 1:
                        page = tnum//10 + 1 if tnum<1000 else 101
                        for p in range(1,page):
                            try:
                                resp = req_get(url + '&p=%d'%(p+1))
                                write_comp(resp)
                            except:
                                line = get_proxy()
                                resp = req_get(url + '&p=%d'%(p+1))
                                write_comp(resp)
                                
                    # 还大于1000条的话，记录该条信息，也可以根据其他筛选条件继续拆分检索
                    if tnum > 1000:
                        out_range.append([pr,lv,yr,ar])

print('超出1000范围')                        
for i in out_range:
    print(i)
out_file.close()
