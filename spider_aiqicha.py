m = '4200005'
mk = 0
# line = get_proxy()
for pr in provs:
    for lv in rcl:
        
#         for ar in list(wdl):
        if str(pr)+str(lv) == m:
            mk = 1
            print(m)
        if mk == 1:
            url0 = 'https://aiqicha.baidu.com/s?q=整容&f={"provinceCode":"%d","regCapLevel":"level%d"}'%(pr,lv)
            
            resp = req_get(url0)


            page_data = re.findall('pageData = ({.*})',resp.text)[0]
            jd = json.loads(page_data)
            tnum = int(jd['result']['totalNumFound'])
            print(tnum, pr, lv)
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
            if tnum > 1000:
                for yr in sy:

                    url = 'https://aiqicha.baidu.com/s?q=整容&f={"provinceCode":"%d","regCapLevel":"level%d","startYear":"%s"}'%(pr,lv,yr)
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
                    if tnum > 1000:
                        print(pr,lv,yr)
