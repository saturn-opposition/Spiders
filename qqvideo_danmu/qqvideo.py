import requests
import json
import csv
from bs4 import BeautifulSoup
page = 15
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
get_url = 'https://v.qq.com/x/cover/vbb35hm6m6da1wc/w0031s4gikk.html'       #修改
responce = requests.get(get_url,headers=headers)
data = responce.content.decode('utf-8')
soup = BeautifulSoup(data,'lxml')
links = soup.find_all('span',attrs={'_stat':'videolist:click'})
link = []
for i in links:
    a = i.find('a')
    link.append(a['href'])
get_url = 'https://v.qq.com/x/cover/vbb35hm6m6da1wc/h003168132m.html'       #修改
responce = requests.get(get_url,headers=headers)
data = responce.content.decode('utf-8')
soup = BeautifulSoup(data,'lxml')
links = soup.find_all('span',attrs={'_stat':'videolist:click'})
for i in links:
    a = i.find('a')
    link.append(a['href'])
postfix = []
for i in link:
    s = i.split('/')[-1]
    postfix.append(s[0:-5])


def each(u,index):
    content = []
    name = []
    upcount = []
    user_degree = []
    timepoint = []
    comment_id = []

    for i in range(0, 86):                                  #修改
        url = u + str(page + 30 * i)
        try:
            responce = requests.get(url, headers=headers)
            data = responce.content.decode('utf-8')
            bs = json.loads(data, strict=False)
            for j in bs['comments']:
                content.append(j['content'])  # 弹幕内容
                name.append(j['opername'])  # 用户名
                upcount.append(j['upcount'])  # 点赞数
                user_degree.append(j['uservip_degree'])  # 会员等级
                timepoint.append(j['timepoint'])  # 发布时间
                comment_id.append(j['commentid'])  # 弹幕ID
        except:
            print(url+'失败')
    header_a = ['内容', '用户', '点赞数', '用户等级', '时间', '弹幕id']
    path = "C:\\Users\\hjn\\Desktop\\爬虫\\陈情令第"+str(index+1)+"集弹幕.csv"       #修改
    with open(path, "w", encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_a)
        csvwriter.writerows(zip(content, name, upcount, user_degree, timepoint, comment_id))
    csvfile.close()
    print('第'+str(index+1)+'集完成')


def get_episode_danmu(v_id, headers):
    # target_id所在基础网址
    base_url = 'https://access.video.qq.com/danmu_manage/regist?vappid=97767206&vsecret=c0bdcbae120669fff425d0ef853674614aa659c605a613a4&raw=1'
    # 传递参数，只需要改变后缀ID
    pay = {"wRegistType": 2, "vecIdList": [v_id],
           "wSpeSource": 0, "bIsGetUserCfg": 1,
           "mapExtData": {v_id: {"strCid": "wu1e7mrffzvibjy", "strLid": ""}}}

    html = requests.post(base_url, data=json.dumps(pay), headers=headers)
    bs = json.loads(html.text)
    # 定位元素
    danmu_key = bs['data']['stMap'][v_id]['strDanMuKey']
    # 解析出target_id
    target_id = danmu_key[danmu_key.find('targetid') + 9: danmu_key.find('vid') - 1]
    return [v_id, target_id]

for p in range(len(postfix)):
    v_id,target_id = get_episode_danmu(postfix[p],headers)
    url = 'https://mfm.video.qq.com/danmu?otype=json&target_id='+str(target_id)+'%26vid%3D'+v_id+'&timestamp='
    each(url,p)

