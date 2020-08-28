import requests
from bs4 import BeautifulSoup
import re
pattrn=re.compile(r'\d{2,3}\.\d{2,3}\.\d{2,3}\.\d{2,3}')

ip=[]

url='https://www.xicidaili.com/nn/'
for i in range(1,100):
    try:
        url='https://www.xicidaili.com/nn/{}'.format(i)
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'}
        response=requests.get(url,headers=headers)
        
        page=response.text
        soup=BeautifulSoup(page,'lxml')
        ip_list=soup.select('table[id="ip_list"]')[0]
        
        trs=ip_list.find_all('tr')[1:]
        for tr in trs:
            tds=tr.find_all('td')
            ip_=tds[1].text+':'+tds[2].text
            ip.append(ip_)
        
with open('ip_list.txt','w') as f:
    for line in ip:
        f.write(line.strip('\n')+'\n')