import requests
import re
import time
from lxml import etree
from fake_useragent import UserAgent
import pymysql
import random
headers = {
    'User-agent' : UserAgent().random,
    'Host' : 'weibo.cn',
    'Accept' : 'application/json, text/plain, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Cookie' :'_T_WM=19915191835; XSRF-TOKEN=0459ac; WEIBOCN_FROM=1110006030; SUB=_2A25zUK-tDeRhGeFN4lsU9y7PyjmIHXVQujHlrDV6PUJbkdANLWygkW1NQ7-6uRZv-EHqzwl4XNmgZUUZohBGz5ry; SUHB=06ZV7w5EoTjCdy; SCF=Anze7S_q3LGw9BaFkuagiYENlakxeqNdyy7awdeNlkErl3k51ZFTTzyFg2gvjlDDPAf3D39P9NOOOhht0KJRVVs.; SSOLoginState=1582620669; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174',
    'DNT' : '1',
    'Connection' : 'keep-alive'
     }#请求头的书写，包括User-agent,Cookie等

def get_one_page(url):#请求函数：获取某一网页上的所有内容

    response = requests.get(url,headers = headers,verify=False)#利用requests.get命令获取网页html
    print(response.status_code)
    if response.status_code == 200:#状态为200即为爬取成功
        return response.content#返回值为html文档，传入到解析函数当中
    return None
def parse_one_page(html,id):#解析html并存入到文档result.txt中
    html = etree.HTML(html)
    comment = []
    user_name = []
    comments = html.xpath('//div[@class=\'c\'][@id]/span[@class=\'ctt\']/text()')[1:]
    user_name = html.xpath('//div[@class=\'c\'][@id]/a[1]/text()')[1:]
    for i in range(len(user_name)):
        if comments[i] == "回复":
            continue
        print(user_name[i]+':'+comments[i])
        cursor.execute("insert into comment(id ,username,text)values(%s, %s,%s)",
                    (id,user_name[i],comments[i]))
        conn.commit()


    # for c in comments:
    #     comment.append(c.xpath('//span[@class=\'ctt\']/text()'))
    #     user_name.append(c.xpath('//a/text()'))
    #     print(comment)
    #     print(user_name)

#
# for i in range(3):
#     url = "https://weibo.cn/comment/Iz3bNkIrD?page="+str(i)
#     html = get_one_page(url)
#     print(html)
#     print('正在爬取第 %d 页评论' % (i+1))
#     parse_one_page(html)
#     time.sleep(3)

# //*[@id="pagelist"]/form/div/text()[2]

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='hjnmysqlmima0930', db='liwenliang')
cursor = conn.cursor()
cursor.execute("select id from weibo where comments_count != 0")
row = cursor.fetchall()
ids = []
for i in range(len(row)):
    ids.append(row[i][0])
print(len(ids))
def run(ids):
    for i in range(4523,5000):
        root_url = "https://weibo.cn/comment/"+ids[i]
        response = requests.get(root_url, headers=headers, verify=False)  # 利用requests.get命令获取网页html
        print(response.status_code)
        try:
            if response.status_code == 200:  # 状态为200即为爬取成功
                html = etree.HTML(response.content)
                page_num_list = html.xpath('//*[@id="pagelist"]/form/div/text()[2]')
                print(page_num_list)
                if page_num_list != []:
                    page_num = int(page_num_list[0].split('/')[1].strip('页'))
                    r = min(page_num+1,50)
                    for j in range(1,r):
                        url = root_url + "?page=" + str(j)
                        html = get_one_page(url)
                        print('正在爬取第 %d 页评论' % (j))
                        parse_one_page(html, ids[i])
                        if j%3 == 0:
                            time.sleep(random.randint(3, 10))
                else:
                    html = get_one_page(root_url)
                    parse_one_page(html, ids[i])
                    # time.sleep(random.randint(3, 10))

            else:
                continue
            
            
            print('********************第'+str(i)+"条微博爬取完毕************************")
        except Exception as e:
            print(e)
    if i % 5 == 0:

        time.sleep(random.randint(10,15))

run(ids)