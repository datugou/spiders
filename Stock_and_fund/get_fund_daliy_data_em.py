import requests
import pandas as pd
import re, time
import akshare as ak

def get_market_id(symbol: str) -> int:
    """
    东方财富-ETF市场标识判断
    :param symbol: ETF 代码
    :type symbol: str
    :return: ETF 代码和市场标识（1:上证 0:深证）
    :rtype: int
    """
    if symbol.startswith(("0", "1", "3", "2", "5", "6")):
        if symbol.startswith(("5", "6")):
            return 1
        else:
            return 0
    else:
        return 1


fund_name_em_df = ak.fund_name_em()


for ind, code in enumerate(fund_name_em_df['基金代码']):
    nc = get_market_id(str(code))
    ncode = nc+'.'+str(code)

    time.sleep(5)
    url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116&klt=101&fqt=1&secid=%s&beg=20000101&end=20260520'%(ncode)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'push2his.eastmoney.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',
        'Cookie': '需要自己获取'
    }
    # 需要自己获取 Cookie 值

    r = requests.get(url, timeout=15, headers=headers)
    # r = requests.get(url, timeout=15)
    data_json = r.json()
    if data_json["data"]:
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = [
            "日期",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["日期"], errors="coerce")
        temp_df.reset_index(inplace=True, drop=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
        temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
        temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"], errors="coerce")
        temp_df['code'] = ncode
    
        fp = r'E:\PythonProject\量化\data_fund\\' + ncode + r'.csv'
        temp_df.to_csv(fp)
        
        print(ind, ncode, end='\r')
