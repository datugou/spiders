# WIPO patentscope 爬虫
2021.04.28

---
只提供了验证码识别的代码。

整体思路如下图。

<div align=center><img src="https://user-images.githubusercontent.com/30107520/116360488-8ea5e500-a832-11eb-968e-89f5a82c8824.png" width = '600'></div>




## 爬虫说明

在 spider_patentscope_crack_captcha.py 中 main() 函数返回带 cookies 的 headers，爬虫直接用该 headers 即可正常获取数据。

cookies 有时效性，并且短时间内多次访问，cookies 也会失效。失效后需要重新获取 cookies。
cookies 失效后，访问会重定向到 'https://patentscope2.wipo.int/search/en/captcha/captcha.jsf' ，可以根据此判断何时更新 cookies。

为了破解 ‘_pk_id.5.5313’ 参数，需要使用PhantomJS，
首先下载它的[驱动](https://phantomjs.org/download.html)，解压后在 bin 文件夹找到 phantomjs.exe，然后把它放下Python代码统一目录下。

`piwik_.js` 文件为 ‘_pk_id.5.5313’ 参数的 js 脚本。不懂 js，看起来像是个时间戳，不知道能不能用 python 代码替换。

### 获取验证码答案思路
验证码的问题类似“写出每张图片有几只猫”，“标记每张图片是不是有雪”等等。
测试发现验证问题、以及图片都是固定的几个；每次的图片链接的是随机的生成的。
所以思路就是把所有验证问题和图片都获取，然后为每个图片做好标记，存储在本地。
后续验证时，下载当前的图片，然后与本地存的图片比较，就能得到验证码的答案。

`captcha_img_data` 文件为所有验证码图片的标记数据，经过图片对比算法变成了 hash 值。


下载的视频保存在以抖音用户名为名程的文件夹里。

---
[返回首页](https://github.com/datugou/spiders)
