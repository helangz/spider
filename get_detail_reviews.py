import requests
from bs4 import BeautifulSoup
import timeimport requests
from bs4 import BeautifulSoup
import time
import re
from functools import reduce
import random
import pandas as pd
import csv
#将文件写入clown


def get_ip_list():
    with open('e:/tripadvisorSpider/ip_list.txt','r') as f:
        ip_list=f.readlines()
    return ip_list

#列表分割
def chunks(id_lists,n=20):
    """Yield successive n-sized chunks from l."""
    chunks_lists=[]
    for i in range(0,len(id_lists),n):
        slices=id_lists[i:i+n]
        chunks_lists.append(slices)
    return chunks_lists



def get_reviews(id_list,clown,median,ip_list):
    time.sleep(3)
    r1=id_list[0]
    r2=reduce(lambda x,y: x+','+y,id_list)
    #构造url
    url='https://www.tripadvisor.cn/ExpandedUserReviews-{}?target={}&context=1&reviews={}&servlet=Hotel_Review&expand=1'.format(median,r1,r2)

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
    try:
        s=requests.session()
        response=s.get(url,headers=headers,timeout=(20,50),proxies=proxies)
        page=response.text
        soup=BeautifulSoup(page,'lxml')
        if response.status_code!=200:
            print(response.status_code)

        #参看与该ID有关的评论
        for user_id in id_list:
            try:
                e_id='expanded_review_'+user_id
                select_element='div[id='+'"'+e_id+'"'+']'
                reviews=soup.select(select_element)[0]
                #获取时间，key_word，和详细评论
                key_word=reviews.select('span[class="noQuotes"]')[0].text
                date=reviews.select('span[class="ratingDate"]')[0].text
                review_text=reviews.select('div[class="entry"] p')[0].text
                rate_text=str(reviews.select('div[class="rating reviewItemInline"]')[0])
                #获取总评分
                total_rate=re.findall('ui_bubble_rating bubble_(\d+)',rate_text)[0]
                #获取入住类型
                if reviews.select('span[class="recommend-titleInline"]'):
                    room_type=reviews.select('span[class="recommend-titleInline"]')[0].text
                else:
                    room_type=''
                #获取更细粒度的
                aspect={}
                rule_score=re.compile('bubble_(\d+)')
                if reviews.select('div[class="rating-list"]'):
                    review_detail=reviews.select('div[class="rating-list"]')[0]
                    details=review_detail.select('li[class="recommend-answer"]')
                    for detail in details:
                        if detail:

                            score=rule_score.findall(str(detail))
                            aspect[detail.text]=score
                clown.append([user_id,review_text,total_rate,key_word,date,room_type,aspect,median])
            except:
                print('******failed_crawl_user_id*************')
                error_id.appen(str(user_id)+'****'+median)
                break
    except:
        print('**********somethingwrong***********')
        error_id_list.append([str(id_list)+'****'+median for id_list in id_lists])

def write_to_csv(clown,name):
    with open("./{}.csv".format(name),"a",newline="",encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile,dialect = ("excel"))
        for line in clown:
            csvwriter.writerow(line)
def write_error_id(error_id,error_id_list):
    with open('./error_id2.txt','a') as f:
        for line in error_id:
            f.write(line+'\n')
        for lines in error_id_list:
            for line in lines:
                f.write(line+'\n')
def chick_id(id_list):
    lists=[]
    for user_id in id_list:
        user_id=str(user_id)
#        user_id=user_id.strip('\n')
        if   re.findall('\d+',user_id):
            lists.append(user_id)
    return lists


#clown=[['user_id','review_text','total_rate','key_word','date','room_type','aspect','median']]
#clown=[]
error_id=[]
error_id_list=[]
#获取ID列表
# with open('f://error_id.txt','r') as f:
#     id_lists=list(set(f.readlines()))
total_data=pd.read_csv('./uid.csv',names=['user_id','median','hotel_name'])



group_data=total_data.groupby(['median'])
group_list=[]
for name,group in group_data:
    group_list.append(group.reset_index(drop=True))


ip_list=get_ip_list()
for num,data in enumerate(group_list):
    clown=[['user_id','review_text','total_rate','key_word','date','room_type','aspect','median']]
    id_lists=data['user_id']
    median=data['median'][1]
    name=data['hotel_name'][1]
    
    id_lists=list(set(id_lists))
    id_lists=chunks(id_lists)
    print('************startcrawl--{}***********'.format(name))
    print('******group_num***********{}****'.format(num))
    for i in range(len(id_lists)):
        id_list=id_lists[i]
        id_list=chick_id(id_list)
        get_reviews(id_list,clown,median,ip_list)
        print(i)
    print('*********startwrite*************')
    write_to_csv(clown,name)
    write_error_id(error_id,error_id_list)
