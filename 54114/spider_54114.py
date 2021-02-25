import requests, re, json, csv
from bs4 import BeautifulSoup

url_h = 'http://m.54114.cn'


# 获取行业二级目录
hy = {}
tree = []
for i in range(1,116):
    resp = requests.get('http://m.54114.cn/hangye%d/'%(i))
    sp = BeautifulSoup(resp.text)
    while 'Timeout' in sp.get_text():
        resp = requests.get('http://m.54114.cn/hangye%d/'%(i))
        sp = BeautifulSoup(resp.text)
    fi = sp.find_all('div',class_ = 'am-breadcrumb')[0].find_all('a')[-1].get('href')
    fin = sp.find_all('div',class_ = 'am-breadcrumb')[0].find_all('a')[-1].get_text()
    hy[fi] = fin
    si =[i.get('href') for i in sp.find_all('div',class_='boxcontent')[0].find_all('a')]
    if fi not in si:
        tree.append([fi,si])
tree = [(i[0],j) for i in tree for j in i[1]]        
t1 = [i[0] for i in tree]
t2 = [i[1] for i in tree]
for i,v in hy.items():
    if i not in t1:
        if i not in t2:
            tree.append((i,i))

            
# 获取省份城市目录
resp = requests.get('http://m.54114.cn/beijing/')
bs = BeautifulSoup(resp.text)
provs = [[i.div.get_text(), j.a.get_text(), j.a.get('href')] for i in bs.find_all('dl', class_='listtxtcity') for j in i.find_all('dd')]


# 抓取所有企业详情页链接
data_dir = []
# 用于记录访问错误链接
error_url = []
total = len(provs)*len(tree)
cur = 0
for ct in provs:
    for fi in tree:
        for pg in range(1,99999):
            cur += 1
            print('正在抓取企业目录，当前进度：',cur,'/',total, end="\r")
            url = 'http://m.54114.cn/%s/%s_p%d/'%(ct[-1].replace('/',''),fi[-1].replace('/',''),pg)
            try:
                linfo = requests.get(url).text
            except:
                print('错误',url)
                error_url.append(url)
                continue
            gsinfos = re.findall('href="(/.+html)"', linfo)
            nminfos = re.findall('html" title="(.*?)"',linfo)
            if len(gsinfos) == 0:
                break
            for i in range(len(gsinfos)):
                data_dir.append([ct[0],ct[1],hy[fi[0]],hy[fi[1]],gsinfos[i],nminfos[i]])
print('正在抓取企业目录，当前进度：',cur,'/',total)        


# 抓取所有企业详情页内容
data_dict = {}
total = len(data_dir)
cur = 0
for i in data_dir:
    cur += 1
    print('正在抓取详情页，进度：',cur,'/',total, end="\r")
    data_dict[i[-1]] = {}
    data_dict[i[-1]]['省份'] = i[0]
    data_dict[i[-1]]['城市'] = i[1]
    data_dict[i[-1]]['一级行业'] = i[2]
    data_dict[i[-1]]['二级行业'] = i[3]
    data_dict[i[-1]]['链接'] = i[4]
    data_dict[i[-1]]['法定代表人'] = ''
    data_dict[i[-1]]['电话'] = ''
    data_dict[i[-1]]['邮箱'] = ''
    data_dict[i[-1]]['网址'] = ''
    data_dict[i[-1]]['地址'] = ''
    data_dict[i[-1]]['经营范围'] = ''
    data_dict[i[-1]]['公司简介'] = prs[1].get_text().strip()
    
    info = requests.get(url_h+i[-2]).text
    sp = BeautifulSoup(info)
    prs = sp.find_all('div', class_='hynav2')
    for row in prs[0].find_all('li'):
        span = row.get_text().strip().split('：')
        data_dict[i[-1]][span[0]] = span[1]      
print('正在抓取详情页，进度：',cur,'/',total)


# 保存数据
with open(r'保存地址\data.csv', 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['公司','省份''城市','一级行业','二级行业','链接','法定代表人','电话','邮箱','网址','地址','经营范围','公司简介'])
    for i in data_dict:
        csv_writer.writerow([i]+list(data_dict[i].values()))



