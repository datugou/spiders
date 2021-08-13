import os

import execjs
import win32clipboard as wc
import requests
import cv2
from bs4 import BeautifulSoup

url_home = 'https://patentscope2.wipo.int'
img_data = r'captcha_img_data'
js_path = r'piwik_.js'

img_data_dic = {}
with open(img_data, 'r', encoding='utf-8') as f:
    for i in f.readlines():
        j = img_data_dic.get(i.split()[0], {}) 
        j[i.split()[2]] = i.split()[1]
        img_data_dic[i.split()[0]] = j

def aHash(img):
    # 获取图片Hash值
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    s = 0
    hash_str = ''
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    avg = s / 64

    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def cmpHash(hash1, hash2):
    # Hash值相似性，值越小越相似
    n = 0
    if len(hash1) != len(hash2):
        return -1

    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def get_ori_cookie():
    resp = requests.get('https://patentscope2.wipo.int/search/en/search.jsf')
    cookie = resp.headers['Set-Cookie']
        
    os.environ["EXECJS_RUNTIME"] = "PhantomJS"
    node = execjs.get()
    ctx = node.compile(open(js_path).read())
    params = ctx.eval('asdfg()')
    
    cookie = '%s; _pk_ses.5.5313=1; _pk_id.5.5313=%s'%(cookie,params)
    print(cookie)
    
    return cookie

def get_tmeporary_cookie(chaptcha, viewstate, headers, rep=5):
    '''
    提交验证码答案，获取临时cookie的值
    '''
    u_ans = 'https://patentscope2.wipo.int/search/en/captcha/captcha.jsf'
    ans_data = {
        # 'javax.faces.partial.ajax': 'true',
        # 'javax.faces.source': 'captchaForm:SUBMIT',
        # 'javax.faces.partial.execute': 'captchaForm',
        # 'javax.faces.partial.render': 'captchaForm',
        # 'captchaForm:SUBMIT': 'captchaForm:SUBMIT',
        'captchaForm': 'captchaForm',
        # 'captchaForm:j_idt989:input': chaptcha,
        'captchaForm:j_idt1104:input': chaptcha,
        'captchaForm:SUBMIT': '',
        'javax.faces.ViewState': viewstate
    }
    resp = requests.post(u_ans, headers=headers, data=ans_data, allow_redirects=False)
    
    if  ('set-cookie' in resp.headers) and ('PS2_' in resp.headers['Set-Cookie']):
        print(resp.headers['Set-Cookie'])
        # print(rep)
        return resp.headers['Set-Cookie'].split(';')[0]    
    else:
        img_urls = []
        sp = BeautifulSoup(resp.content)
        question = sp.find_all('span', class_='b-input__label')[0]
        # print(question.get_text())
        qt = question.get_text().replace(' ', '_')
        pics = sp.find_all('img', class_='b-input-checkbox-img')
        pics = sp.find_all('img')
        #     viewstate = re.findall('ViewState:0.*value=\"([0-9\-:]*)\"',resp.text)[0]
        for i in pics:
            img_urls.append(url_home + i.get('src'))
        chaptcha = get_chaptcha_answer(qt, img_urls, headers)

        rep -= 1
        if rep >= 0:
            return get_tmeporary_cookie(chaptcha, viewstate, headers, rep)
        else:
            print('无法破解验证码，可能验证码图形库更换了')
            raise


def get_chaptcha_answer(qt, img_urls, headers):
    '''
    得到验证码的答案
    '''


    def get_img_value(qt, img_url):
        imgreq = requests.get(img_url, headers=headers)

        img1 = np.frombuffer(imgreq.content, np.uint8)
        img1 = cv2.imdecode(img1, cv2.IMREAD_ANYCOLOR)

        hash1 = aHash(img1)

        for hash0 in img_data_dic[qt]:
            n = cmpHash(hash0, hash1)
            if n <= 3:
                return img_data_dic[qt][hash0]
        return '0'

    if qt == 'Please_add_the_following_numbers_up':
        res = 0
        for img_url in img_urls:
            res += int(get_img_value(qt, img_url))
        res = str(res)
    elif qt == 'Please_write_the_following_number':
        res = ''
        for img_url in img_urls:
            res += get_img_value(qt, img_url)
    else:
        res = ''
        for img_url in img_urls:
            res += get_img_value(qt, img_url) + ','
        res = res[:-1]
    print(qt,res)
    return res

def get_tp_cookie(cookie):
    headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'Cookie': cookie
                }
    resp = requests.get('https://patentscope2.wipo.int/search/en/captcha/captcha.jsf', headers=headers)
    viewstate = re.findall('ViewState:0.*value=\"([0-9\-:]*)\"',resp.text)[0]

    img_urls = []
    sp = BeautifulSoup(resp.content)
    question = sp.find_all('span',class_='b-input__label')[0]
    qt = question.get_text().replace(' ','_')
    # pics = sp.find_all('img',class_='b-input-checkbox-img')
    pics = sp.find_all('img')

    for i in pics:
        img_urls.append(url_home + i.get('src'))

    chaptcha = get_chaptcha_answer(qt, img_urls, headers)
    tp_cookie = get_tmeporary_cookie(chaptcha, viewstate, headers)

    return tp_cookie
    
def main():
    cookie = get_ori_cookie()
    tp_cookie = get_tp_cookie(cookie)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': cookie + '; ' + tp_cookie
    }
    return headers
