import requests
from bs4 import BeautifulSoup
#用户信息：昵称、等级、会员、投稿数、频道数、收藏数、订阅番剧名、关注数、粉丝数、播放数、阅读数、生日
import random

import datetime
import time
ip_pool = {}
def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))

    return current_milli_time()
def getsource(url):
    payload = {
        '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
        'mid': url.replace('https://space.bilibili.com/', '')
    }
    ua = random.choice(uas)
    head = {
        'User-Agent': ua,
        'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
    }
    jscontent = requests \
        .session() \
        .post('http://space.bilibili.com/ajax/member/GetInfo',
              headers=head,
              data=payload,
              proxies=proxies) \
        .text
    time2 = time.time()
    try:
        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                mid = jsData['mid']
                name = jsData['name']
                sex = jsData['sex']
                rank = jsData['rank']
                face = jsData['face']
                regtimestamp = jsData['regtime']
                regtime_local = time.localtime(regtimestamp)
                regtime = time.strftime("%Y-%m-%d %H:%M:%S", regtime_local)
                spacesta = jsData['spacesta']
                birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                sign = jsData['sign']
                level = jsData['level_info']['current_level']
                OfficialVerifyType = jsData['official_verify']['type']
                OfficialVerifyDesc = jsData['official_verify']['desc']
                vipType = jsData['vip']['vipType']
                vipStatus = jsData['vip']['vipStatus']
                toutu = jsData['toutu']
                toutuId = jsData['toutuId']
                coins = jsData['coins']
                print("Succeed get user info: " + str(mid) + "\t" + str(time2 - time1))
                try:
                    res = requests.get(
                        'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp').text
                    viewinfo = requests.get(
                        'https://api.bilibili.com/x/space/upstat?mid=' + str(mid) + '&jsonp=jsonp').text
                    js_fans_data = json.loads(res)
                    js_viewdata = json.loads(viewinfo)
                    following = js_fans_data['data']['following']
                    fans = js_fans_data['data']['follower']
                    archiveview = js_viewdata['data']['archive']['view']
                    article = js_viewdata['data']['article']['view']
                except:
                    following = 0
                    fans = 0
                    archiveview = 0
                    article = 0
            else:
                print('no data now')
            try:
                # Please write your MySQL's information.
                conn = pymysql.connect(
                    host='localhost', user='root', passwd='123456', db='bilibili', charset='utf8')
                cur = conn.cursor()
                cur.execute('INSERT INTO bilibili_user_info(mid, name, sex, rank, face, regtime, spacesta, \
                            birthday, sign, level, OfficialVerifyType, OfficialVerifyDesc, vipType, vipStatus, \
                            toutu, toutuId, coins, following, fans ,archiveview, article) \
                VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",\
                        "%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s")'
                            %
                            (mid, name, sex, rank, face, regtime, spacesta, \
                             birthday, sign, level, OfficialVerifyType, OfficialVerifyDesc, vipType, vipStatus, \
                             toutu, toutuId, coins, following, fans, archiveview, article))
                conn.commit()
            except Exception as e:
                print(e)
        else:
            print("Error: " + url)
    except Exception as e:
        print(e)
        pass


def get_IP_pool():
    url = 'https://www.kuaidaili.com/free/inha/1'
    global ip_pool
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    responce = requests.get(url, headers=headers)
    data = responce.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    tr = soup.find_all('tr')
    for j in range(1, len(tr)):
        td = tr[j].find_all('td')

        ip_pool[str(td[0].text)] = str(td[1].text)


    url = 'https://www.xicidaili.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    responce = requests.get(url, headers=headers)
    data = responce.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    tr = soup.find_all('tr', attrs={'class': 'odd'})
    for j in range(len(tr)):
        td = tr[j].find_all('td')
        ip_pool[str(td[1].text)] = str(td[2].text)

    with open(r"C:\Users\hjn\Desktop\爬虫\免费代理ip.txt", 'r', encoding='utf-8') as f:
        for line in f:
            t = line.split()
            ip_pool[t[0]] = t[1]

    url = 'http://www.iphai.com/free/ng'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://space.bilibili.com/45388',
        'Origin': 'http://space.bilibili.com',
        'Host': 'space.bilibili.com',
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }

    responce = requests.get(url, headers=headers)
    data = responce.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    tr = soup.find_all('tr')
    for j in range(1, len(tr)):
        td = tr[j].find_all('td')
        a = td[0].text.strip()
        b = td[1].text.strip()
        ip_pool[a] = str(b)


head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',

}
root_url = 'https://m.bilibili.com/space/'
uid_list = []
get_IP_pool()
proxy_dict = ip_pool
proxy_list = []
for k,v in proxy_dict.items():
    proxy_list.append(str(k)+':'+str(v))


while (len(uid_list)!=5):
    proxy = random.choice(proxy_list)
    print(proxy)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    random_id = random.choice(range(1,10000000))
    print(random_id)
    url = root_url + str(random_id)
    try:
        responce = requests.get(url,headers=head,proxies = proxies,timeout=2)
        data = responce.content.decode('utf-8')
        soup = BeautifulSoup(data,'lxml')
        print(data)
        uid_list.append(random_id)
    except requests.exceptions.ConnectionError as e:
        pass

