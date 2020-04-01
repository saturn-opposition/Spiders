import requests
from bs4 import BeautifulSoup


url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=65510391'
responce = requests.get(url)
data = responce.content.decode('utf-8')
soup = BeautifulSoup(data,'lxml')
d = soup.find_all('d')
danmu = []


with open(r"C:\Users\hjn\Desktop\爬虫\B站弹幕.txt", "w", encoding='utf-8') as file:
    for i in d:
        file.write(i.text+'\n')