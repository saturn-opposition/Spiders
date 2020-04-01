import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
import re

try:
    browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    browser.get("https://passport.weibo.cn/signin/login")
    time.sleep(3)
    username = browser.find_element_by_css_selector('#loginName')
    time.sleep(2)
    username.clear()
    username.send_keys('17061061662')
    password = browser.find_element_by_css_selector('#loginPassword')
    time.sleep(2)
    password.send_keys('1qscpdrv')
    browser.find_element_by_css_selector('#loginAction').click()
    time.sleep(15)
except:
    print("#####################Error!##############################")
finally:
    print("登录成功！")
url = 'https://weibo.cn/jiangnan?page='
time.sleep(10)
page_size = 25
text = []
dianzan = []
zhuanfa = []
pinglun = []
for i in range(1,page_size+1):
    try:
        new_url = url + str(i)
        browser.get(new_url)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        print(browser.page_source)
        weibo = soup.find_all('div', attrs={'class': 'c'})[1:-1]

        for j in weibo:
            t = j.find_all('span')

            for k in t:
                if k['class'] == ['ctt']:
                    text.append(k.text)
                    print(k.text)
            z = j.find_all('a')

            for k in z:
                if '赞' in k.text:
                    dianzan.append(re.sub("\D", "", k.text))
                if '转发' in k.text:
                    zhuanfa.append(re.sub("\D", "", k.text))
                if ('评论' in k.text) & ('原文评论' not in k.text):
                    pinglun.append(re.sub("\D", "", k.text))
    except:
        print('爬取第'+str(i)+'页微博出错')
header_a = [ '内容', '点赞数','转发数','评论数']
with open(r"C:\Users\hjn\Desktop\爬虫\江南微博.csv", "w", encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_a)
        csvwriter.writerows(zip(text,dianzan,zhuanfa,pinglun))
csvfile.close()





# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# }
#
# url_root = 'https://m.weibo.cn/u/2706896955?uid=2706896955'
# responce = requests.get(url_root,headers=headers)
# data = responce.content.decode('utf-8')
# with open(r"C:\Users\hjn\Desktop\爬虫\zyx.html", "w", encoding='utf-8')as f:
#     f.write(data)
# soup = BeautifulSoup(data,'lxml')
# text = soup.find_all('div',attrs={'class':'weibo-text'})
# for i in text:
#     print(i.string)