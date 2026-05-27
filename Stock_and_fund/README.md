# 股票基金爬虫
2026.05.27

---
免费的数据可以从 AKshare 这个库获取。

AKshare 中，部分东方财富网的数据接口不能用了，东方财富网现在有反爬措施。


## 个股板块信息

### [东方财富网个股板块信息](https://github.com/datugou/spiders/blob/main/Stock_and_fund/get_stock_board.py) 2026.05.27

根据股票代码，获取股票的板块信息。

所有股票代码用 AKshare 的 stock_zh_a_spot() 方法获取。


## 基金每日行情数据 

东方财富的数据接口不能用。

新浪财经的数据接口（fund_etf_category_sina()）只有 1500 个 ETF / LOF / 封闭式基金的数据（OHLC（开盘、最高、最低、收盘）），没有普通场外开放式基金（仅净值）的数据。

### [东方财富网基金每日行情数据](https://github.com/datugou/spiders/blob/main/Stock_and_fund/get_fund_daliy_data_em.py) 2026.05.27

这个有反爬，开始需要访问主页获取 Cookie 值。

之后单位时间超过一定访问次数就会触发反爬。

触发后需要访问主页完成滑块验证，然后更新 Cookie。

这个爬虫没有完成滑块验证这部分代码，我用的时候试了一下新浪网的数据，那边没有反爬，所以这个东方财富的爬虫就没完善。

自己用时候是在浏览器上把 Cookie 抠出来粘到爬虫代码中的。

### [新浪财经网基金每日行情数据](https://github.com/datugou/spiders/blob/main/Stock_and_fund/get_fund_daliy_data_sina.py) 2026.05.27

这个只有每日净值数据，没有 OHLC（开盘、最高、最低、收盘）数据。

每次访问只能获取 20 个交易日的净值数据，最好开多线程下载，但是也很慢，全部基金有 26000 多个，我下完用了 4 天。

## 基金重仓股数据 

### [新浪财经网基金十大重仓股数据](https://github.com/datugou/spiders/blob/main/Stock_and_fund/get_fund_sdzc_sina.py) 2026.05.27

获取基金十大重仓股的股票代码和占比。

---
[返回首页](https://github.com/datugou/spiders)
