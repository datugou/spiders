import requests,re,json

r = requests.get('http://m.54114.cn/beijing/')

r.text
dzl = re.findall('a href="/([a-z]+)/"',r.text)

outfile = open(r'D:\data\114_url.txt','w') 

mk = 0
mkk = 0
wd = 'beijing88'
for cs in dzl:
    for rg in range(1,116):
        if cs+str(rg) == wd:
            mk = 1
        if mk == 1:
            for pg in range(99999):
                print(cs,rg,pg)
                if pg == 477:
                    mkk = 1
                if mkk == 1:
                    url = 'http://m.54114.cn/%s/hangye%d_p%d/'%(cs,rg,pg)
                    try:
                        linfo = requests.get(url).text
                    except:
                        continue
                    gsinfos = re.findall('href="(/.+html)"', linfo)
                    nminfos = re.findall('html" title="(.*?)"',linfo)
                    if len(gsinfos) == 0:
                        break
                    for i in range(len(gsinfos)):
                        outfile.write(cs+':'+gsinfos[i]+':'+nminfos[i]+'\n')
                        
linfo = requests.get(url)

urls = re.findall('href="(/.+html)"', linfo.text)
cnms = re.findall('html" title="(.*?)"',linfo.text)
lxrs = re.findall('>联系人：(.*?)<',linfo.text)
tels = re.findall('电话：(.*?)</b',linfo.text)
tels = [';'.join(re.findall('href="tel:(.*?)"',i)) for i in tels]
adds = re.findall('>地址：(.*?)<',linfo.text)

url = 'http://m.54114.cn/so1116/'

len(urls),len(cnms),len(lxrs),len(tels),len(adds)

for i in range(len(urls)):
    print(urls[i],cnms[i],lxrs[i],tels[i],adds[i])
    
    
tr = requests.get('http://m.54114.cn/hangye3')   
sp = BeautifulSoup(tr.text)
from bs4 import BeautifulSoup

hy = []
tree = []

for i in range(1,116):
    resp = requests.get('http://m.54114.cn/hangye%d/'%(i))
    sp = BeautifulSoup(resp.text)
    while 'Timeout' in sp.get_text():
        resp = requests.get('http://m.54114.cn/hangye%d/'%(i))
        sp = BeautifulSoup(resp.text)
    fi = sp.find_all('div',class_ = 'am-breadcrumb')[0].find_all('a')[-1].get('href')
    fin = sp.find_all('div',class_ = 'am-breadcrumb')[0].find_all('a')[-1].get_text()
    hy.append((fi, fin))
    si =[i.get('href') for i in sp.find_all('div',class_='boxcontent')[0].find_all('a')]
    if fi not in si:
        tree.append([fi,si])
        
tree = [(i[0],j) for i in tree for j in i[1]]        
t1 = [i[0] for i in tree]
t2 = [i[1] for i in tree]
for i in hy:
    if i[0] not in t1:
        if i[0] not in t2:
            tree.append((i[0],i[0]))
t2 = [i[1] for i in tree]  

# 获取城市列表
resp = requests.get('http://m.54114.cn/beijing/')
cities = re.findall('a href="/([a-z]+)/"',resp.text)

for ct in cities:
    for hyn in t2:
        for pg in range(99999):
            url = 'http://m.54114.cn/%s/%s_p%d/'%(ct,hyn.replace('/',''),pg)
            try:
                linfo = requests.get(url).text
            except:
                continue
            gsinfos = re.findall('href="(/.+html)"', linfo)
            nminfos = re.findall('html" title="(.*?)"',linfo)
            if len(gsinfos) == 0:
                break
            for i in range(len(gsinfos)):
                outfile.write(cs+':'+gsinfos[i]+':'+nminfos[i]+'\n')
                
                
'/hangye24/' in tree[0][1]
'Timeout' in sp.get_text()
