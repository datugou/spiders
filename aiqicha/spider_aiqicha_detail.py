import re,json,time
import requests
from bs4 import BeautifulSoup

def get_proxy()
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
        outFile.write(asp+'\n')
        

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


# 有代理池的把use_proxy的值改成1
use_proxy = 0

# 加载search_result爬到的数据
with open(r'D:\data.txt','r') as f:
    ac = f.readlines()
    pids = [json.loads(i)['pid'] for i in f.readlines()]
    total = len(ac)
out_file = open(r'D:\data_detail.txt','a')

if use_proxy == 1:
    line = get_proxy()
    req_get = req_get_proxy

error_pid = []    
j = 0    
for pid in pids:
    rsp = req_get('https://aiqicha.baidu.com/detail/basicAllDataAjax?pid=%s'%(pid))
    jd = json.loads(rsp.text)

    if '系统异常' in jd['msg']:
        error_pid.append(pid)
    else:
        out_file.write(rsp.text)
    j += 1
    print('\r'+str(j)+'/'+str(total),end = "")
print('\n')
print('未下载公司pid')
for i in error_pid:
  print(i)

