import requests
from bs4 import BeautifulSoup
import time
import re
import random
import csv
ip_path='e:/tripadvisorSpider/ip_list.txt'
href_path='./href_list.txt'
save_path='./uid.csv'
def get_ip_list():
    with open(ip_path,'r') as f:
        ip_list=f.readlines()
    return ip_list

def get_url_list():
    with open(href_path,'r')  as f:
        readlines=f.readlines()
        url_list=[line.strip('\n') for line in readlines]
    return url_list

    
def get_uid(url,ip_list,clown):
    user_agent_pools=[
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
     ]
    ip=random.choice(ip_list)
    user_agent=random.choice(user_agent_pools)
    proxies={'http':'http://'+ip}
    headers={'User-Agent': user_agent,
            'Cookie':'TASSK=enc%3AAF2f1Anf6qgv%2BlAqVy%2Fofj%2BJ1YD%2BD%2FxKNueO54Ib8zdk%2FqAF%2Fwz2fixggRI2YS0Gf9EiOzMKqVMWGf%2B4v%2FeX5kQSocgGHkk79CM%2Fu1eHRNrP5bvfhHq5sQ31rrP%2FAcMSCA%3D%3D; TART=%1%enc%3A8qE0F38a3xmdW9Ko%2Fp9tf4LK5Oo1Chimw3%2Bbl9nB9g0gyXeBQd3kwDUovLW9NS1fkagyFvowwb0%3D; TATravelInfo=V2*AY.2018*AM.12*AD.30*DY.2018*DM.12*DD.31*A.2*MG.-1*HP.2*FL.3*DSM.1545125686589*RS.1; TAUD=LA-1545100554558-1*RDD-1-2018_12_18*HC-25125489*HDD-25154934-2018_12_30.2018_12_31.1*LD-117757340-2018.12.30.2018.12.31*LG-117757342-2.1.F.; TAUnique=%1%enc%3A2cU7ADHy9EonhwOm5c3w0GYodE1BwtD%2Bain6NbTfRTg%3D; _ga=GA1.2.1947034738.1545100554; _gid=GA1.2.1589299958.1545100554; TALanguage=en; __gads=ID=10b67d669da03a35:T=1545132305:S=ALNI_Ma8WqqyixvxLmxR18JbbNkw3VHnuA; TASession=%1%V2ID.C988D4402CB376E68D6435B4E5A5A6B0*SQ.44*LP.%2FHotel_Review-g186338-d1657415-Reviews-Park_Plaza_Westminster_Bridge_London-London_England%5C.html*LS.DemandLoadAjax*GR.10*TCPAR.38*TBR.80*EXEX.60*ABTR.53*PHTB.68*FS.16*CPU.80*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*FLO.1657415*TRA.false*LD.1657415; ServerPool=C; TAReturnTo=%1%%2FHotel_Review-g186338-d1657415-Reviews-or20-Park_Plaza_Westminster_Bridge_London-London_England.html; BEPIN=%1%167c5559b09%3Busr03t.daodao.com%3A10023%3B; roybatty=TNI1625!AN9hj2jKZ6Hd4K2FrC%2FoUvHjmNcmZRKnm8CbzB5a1e1sNlOheVBT0z4BW%2FfFwXU0zcsWTRDNi3j96jFbLLr8T1SvQ6Wk1lU8nPmco3WzUE8pCe6kBpVrhWDzPpdypkGESTPo%2Fc8saho2Q4jmT9mhEgXpYneFr1qcswv8wq5ODKNg%2C1; _gat_UA-79743238-4=1'

            }

    time.sleep(5)
    s=requests.session()
    try:
        response=s.get(url,headers=headers,timeout=(20,50),proxies=proxies)
        if response.status_code!=200:
            print(response.status_code)

        page=response.text
        soup=BeautifulSoup(page,'lxml')
        review_lists=soup.select('div[class="listContainer hide-more-mobile"] div[class="review-container"]')

        for reviews in review_lists:
            user_id=reviews['data-reviewid']
            # span=reviews.select('div[class="ui_column is-9"] span')
            # total_score=span[0]['class'][-1].split('_')[-1]
            # key_word=span[2].text
            # date=span[1]['title']
            # review_text=reviews.select('p[class="partial_entry"]')[0].text
            clown.append(user_id)
        print(len(clown))
    except:
        print('time error')

def get_page_num(url,clown):

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Cookie':'TASSK=enc%3AAF2f1Anf6qgv%2BlAqVy%2Fofj%2BJ1YD%2BD%2FxKNueO54Ib8zdk%2FqAF%2Fwz2fixggRI2YS0Gf9EiOzMKqVMWGf%2B4v%2FeX5kQSocgGHkk79CM%2Fu1eHRNrP5bvfhHq5sQ31rrP%2FAcMSCA%3D%3D; TART=%1%enc%3A8qE0F38a3xmdW9Ko%2Fp9tf4LK5Oo1Chimw3%2Bbl9nB9g0gyXeBQd3kwDUovLW9NS1fkagyFvowwb0%3D; TATravelInfo=V2*AY.2018*AM.12*AD.30*DY.2018*DM.12*DD.31*A.2*MG.-1*HP.2*FL.3*DSM.1545125686589*RS.1; TAUD=LA-1545100554558-1*RDD-1-2018_12_18*HC-25125489*HDD-25154934-2018_12_30.2018_12_31.1*LD-117757340-2018.12.30.2018.12.31*LG-117757342-2.1.F.; TAUnique=%1%enc%3A2cU7ADHy9EonhwOm5c3w0GYodE1BwtD%2Bain6NbTfRTg%3D; _ga=GA1.2.1947034738.1545100554; _gid=GA1.2.1589299958.1545100554; TALanguage=en; __gads=ID=10b67d669da03a35:T=1545132305:S=ALNI_Ma8WqqyixvxLmxR18JbbNkw3VHnuA; TASession=%1%V2ID.C988D4402CB376E68D6435B4E5A5A6B0*SQ.44*LP.%2FHotel_Review-g186338-d1657415-Reviews-Park_Plaza_Westminster_Bridge_London-London_England%5C.html*LS.DemandLoadAjax*GR.10*TCPAR.38*TBR.80*EXEX.60*ABTR.53*PHTB.68*FS.16*CPU.80*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*FLO.1657415*TRA.false*LD.1657415; ServerPool=C; TAReturnTo=%1%%2FHotel_Review-g186338-d1657415-Reviews-or20-Park_Plaza_Westminster_Bridge_London-London_England.html; BEPIN=%1%167c5559b09%3Busr03t.daodao.com%3A10023%3B; roybatty=TNI1625!AN9hj2jKZ6Hd4K2FrC%2FoUvHjmNcmZRKnm8CbzB5a1e1sNlOheVBT0z4BW%2FfFwXU0zcsWTRDNi3j96jFbLLr8T1SvQ6Wk1lU8nPmco3WzUE8pCe6kBpVrhWDzPpdypkGESTPo%2Fc8saho2Q4jmT9mhEgXpYneFr1qcswv8wq5ODKNg%2C1; _gat_UA-79743238-4=1'

            }
    time.sleep(5)
    s=requests.session()
    response=s.get(url,headers=headers,timeout=(20,50))
    if response.status_code!=200:
        print(response.status_code)
    page=response.text
    soup=BeautifulSoup(page,'lxml')
    review_lists=soup.select('div[class="listContainer hide-more-mobile"] div[class="review-container"]')
    page_num=soup.select('a[class="pageNum last taLnk "]')[0]['data-page-number']
    for reviews in review_lists:
        user_id=reviews['data-reviewid']
        clown.append(user_id)
    return page_num



def write_to_csv(clown,index_url,hotel_name):
    with open(save_path,"a",newline="",encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile,dialect = ("excel"))
        for line in clown:
            csvwriter.writerow([line,index_url,hotel_name])

def main():
    ip_list=get_ip_list()
    url_list=get_url_list()
    pattern_page=re.compile(r'(-Reviews-)')
    global clown
    for url in url_list:
        print('********{}*********'.format(url))
        clown=[]
        p_url=url.split('-')
        index_url=p_url[1]+'-'+p_url[2]
        hotel_name=p_url[-2]
        page_num=int(get_page_num(url,clown))
        for i in range(1,page_num):
            pattern_page=re.compile(r'(-Reviews-)')
            url_i=re.sub(pattern_page,'-Reviews-or{}-'.format(i*5),url)
            print(url_i)
            get_uid(url_i,ip_list,clown)
            print('********现在进行第{}个*********'.format(i))

        print('*********start_write***********')
        write_to_csv(clown,index_url,hotel_name)
if __name__ == '__main__':
    main()         