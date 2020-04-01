import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.douban.com/group/gua/discussion?start='

title = []
user = []
huiying = []
time = []
for k in range(100):
    new_url = url + str(k*25)
    responce = requests.get(new_url)
    data = responce.content.decode('utf-8')
    soup = BeautifulSoup(data,'lxml')
    table = soup.find('table',attrs={'class':'olt'})
    tr = table.find_all('tr')[1:-1]
    for t in tr:
        ti = t.find_all('td')[0]
        a = ti.find('a').get('title').strip()
        title.append(a)
        u = t.find_all('td')[1]
        user.append(u.text)
        h = t.find_all('td')[2]
        huiying.append(h.text)
        t = u = t.find_all('td')[3]
        time.append(t.text)
    print('第'+str(k)+'页完成')

header_a = [ '标题', '发帖人','回复数','时间']
with open(r"C:\Users\hjn\Desktop\爬虫\豆瓣瓜组.csv", "w", encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_a)
        csvwriter.writerows(zip(title,user,huiying,time))
csvfile.close()


