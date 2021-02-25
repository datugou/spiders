# 抖音爬虫
2021.02.25

---
根据 APP 上用户主页的分享链接，下载该用户所有视频。

该项目参考自：https://github.com/jielundong/douyin-gg

## 爬虫说明

在 APP 上进入用户主页，获取分享链接。

<div align=center><img src="https://user-images.githubusercontent.com/30107520/109177356-ab865380-77c2-11eb-90e9-8f1039b9a155.jpg" width = '300'></div>

在 spider_douyin_videos.py 中填写分享链接，并设置下载地址。

```python
# 填写用户分享链接
users_list = ['https://v.douyin.com/eJDmuLm/']

# 设置下载地址
download_path = r'C:\Users\nm\Desktop'
```

下载的视频保存在以抖音用户名为名程的文件夹里。

---
[返回首页](https://github.com/datugou/spiders)
