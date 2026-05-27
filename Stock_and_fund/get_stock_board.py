import requests
import pandas as pd
import re, json
import akshare as ak

# 获取所有A股股票列表
stock_df = ak.stock_zh_a_spot()
print(f"共 {len(stock_df)} 只股票")

# 东方财富 个股版块信息
# 把数据先存到 txt 中，用 "a" 模式，可以断点续上，如果网络中断了，可以根据 ind 和 code 值续上
with open('infos.txt', 'a', encoding='utf8') as f:
    for ind, code in enumerate(stock_df["代码"]):
        code = code[2:]
        jys = code[:2].upper()
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_CORETHEME_BOARDTYPE&sty=ALL&filter=(SECUCODE="%s.%s")' % (code, jys)
        resp = requests.get(url)
        row = resp.text
        f.write('\n')
        f.write(row)
        print(ind, code, end='\r')

# 东方财富 个股版块信息 抽取
datas = []
with open('infos.txt', 'r', encoding='utf8') as f:
    for row in f.readlines():
        if row.strip():
            jt = json.loads(row.strip())
            for i in jt['result']['data']:
                dl = [i['SECUCODE'],i['SECURITY_NAME_ABBR'],i['BOARD_NAME'],i['BOARD_TYPE'],i['BOARD_LEVEL']]
                datas.append(dl)
                dl = []

df = pd.DataFrame(datas, columns=['CODE', 'NAME', 'BOARD', 'TYPE', 'LEVEL'])
df.to_csv('stocks_board.csv')
