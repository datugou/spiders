import requests
import akshare as ak
import json
import pandas as pd

def get_data(fund_name_df):
    for ind, code in enumerate(fund_name_df):
        code = str(code)
        pg = 0
        br = 0
        ld = []
        for i in range(1000):
            if br == 1:
                break
            pg += 1
            url = 'https://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?&symbol=%s&datefrom=2000-01-01&dateto=2026-05-20&page=%d'%(code, pg)
            r = requests.get(url, timeout=15)
            jd = r.json()
            
            if len(jd["result"]["data"]["data"]) > 0:
                ld += [item for item in jd["result"]["data"]["data"]]
            else:
                br = 1
            print('页码', pg, 'num:', ind, code, '             ',end='\r',)
        fp = r'data_fund_sina\\' + code + r'.csv'
        if len(ld) > 0:
            temp_df = pd.DataFrame(ld)
            temp_df.to_csv(fp)


fund_name_df = ak.fund_name_em()

# 每次访问只能获取 20 个交易日的数据，最好开多线程，但是也很慢。
get_data(fund_name_df)
