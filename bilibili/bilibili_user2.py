from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
import re
import pymysql
#用户信息：昵称、等级、会员、投稿数、频道数、收藏数、订阅番剧名、关注数、粉丝数、生日
import random
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='irlab', db='parliamentdata', charset='utf8')
cursor = conn.cursor()                                                                  #数据库建立连接


uid_list = []
browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
while(len(uid_list)!=1000000):
    try:
        uid = str(random.randint(1,999999999))
        url = "https://space.bilibili.com/"+uid
        browser.get(url)
        time.sleep(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        user_name = soup.find('span', attrs={'id': 'h-name'}).text.strip()
        rank = soup.find('a', attrs={'class': 'h-level m-level'}).get('lvl').strip()
        vip = soup.find('a', attrs={'class': 'h-vipType'}).text.strip()
        span = soup.find_all('span', attrs={'class': 'n-text'})
        tougao = ''
        pindao = ''
        shoucang = ''

        for i in span:
            if i.text == '投稿':
                tougao = i.next_sibling.text.strip()
            if i.text == '频道':
                pindao = i.next_sibling.text.strip()
            if i.text == '收藏':
                shoucang = i.next_sibling.text.strip()

        dingyue_list = []
        div_dingyue = soup.find_all('div', attrs={'class': 'large-item clearfix'})
        for i in div_dingyue:
            a = i.find('a', attrs={'class': 'title'}).text.strip()
            dingyue_list.append(a)
        dingyue_str = ','.join(dingyue_list)
        guanzhu = soup.find('p', attrs={'id': 'n-gz'}).text.strip()
        fensishu = soup.find('a', attrs={'class': 'n-fs'}).text.strip()
        b = soup.find('div', attrs={'class': 'item birthday'})
        birthday = b.find('span', attrs={'class': 'text'}).text.strip()
        # print(
        #     uid + '  ' + user_name + "  " + rank + '  ' + vip + "  " + tougao + '  ' + pindao + '  ' + shoucang + '  ' + dingyue_str + '  ' + guanzhu + '  ' + fensishu + '  ' + birthday)
        uid_list.append(uid)
        row = cursor.execute(
            "insert into bilibili_user(uid ,user_name,rank,vip,tougao,pindao,shoucang,dingyue,guanzhu,fensishu,birthday)values(%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s)",
            (uid ,user_name,rank,vip,tougao,pindao,shoucang,dingyue_str,guanzhu,fensishu,birthday))  # 尚未插入包含国家
        conn.commit()
        print(uid+'已保存')
    except:
        print('###############error##########################')