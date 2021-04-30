import requests
import os, re, json

# 填写用户分享链接
users_list = ['https://v.douyin.com/eJdmuLm/']

# 设置下载地址
download_path = r'C:\Users\nm\Desktop'

headers = {
    'accept-encoding': 'deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}

for user in users_list:
    url = user.strip()
    res = requests.get(url, headers=headers, allow_redirects=False)
    sec_uid = re.findall('sec_uid=(.*?)&',res.headers['Location'])[0]

    user_video_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/"
    user_video_params = {
        'sec_uid': sec_uid,
        'count': '21',
        'max_cursor': '0',
        'aid': '1128',
        '_signature': '2Vx9mxAZh0o-K4Wdv7NFKNlcfY',
        'max_cursor':''
    }

            
    print('正在获取视频链接') 
    video_urls = []
    max_cursor, video_count, user_name = None, 0, None
    while True:
        if max_cursor:
            user_video_params['max_cursor'] = str(max_cursor)
            
        res = requests.get(user_video_url, headers=headers, params=user_video_params)
        js = json.loads(res.text)
        
        if not user_name:
            user_name = js['aweme_list'][0]['author']['nickname']
        for i in js['aweme_list']:
            video_count += 1
            video_urls.append((i['video']['play_addr']['url_list'][0],i['desc']))
        if js.get('has_more'):
                max_cursor = js.get('max_cursor')
        else:
            break
    
    
    user_path = os.getcwd() + '\\' + user_name
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    
    print('开始下载',user_name,'的视频')
    num = len(video_urls)
    cur = 1
    for i in video_urls:
        print(' '*50,end="\r") 
        print('{}/{}'.format(cur, num),end="\r")

        f_n = i[1]
        url = i[0]      
        try:
            down_res = requests.get(url=url, headers=headers, verify=False)
            f_n = download_path + '\\' + f_n + '.mp4'
            with open(f_n,"wb") as code:
                code.write(down_res.content)
        except:
            print('下载失败: ',f_n)
        cur += 1
        
    print('{}/{}'.format(cur-1, num))
    print(user_name, '下载完成')
