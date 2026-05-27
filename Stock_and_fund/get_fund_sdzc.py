import requests
import akshare as ak
import json
import pandas as pd

f_zc = []
und = []

fund_name_em_df = ak.fund_name_em()

for ind, fcode in enumerate(fund_name_em_df['基金代码']):
    
    dr = {'fc': fcode}
    r = requests.get('http://finance.sina.com.cn/fund/quotes/%s/bc.shtml'%(fcode))
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        table = soup.find('table', id='fund_sdzc_table')
        for row in table.tbody.find_all('tr'):
            code = row.find_all('td')[0].a['href'].split('/')[-2]
            per = float(row.find_all('td')[3].text[:-1])*0.01
            dr[code] = per
        f_zc.append(dr)
    except:
        und.append(fcode)
    print(ind, end='\r')

f_c_df = pd.DataFrame(f_zc)
f_c_df.to_csv(r'fund_sdzc.csv'))
