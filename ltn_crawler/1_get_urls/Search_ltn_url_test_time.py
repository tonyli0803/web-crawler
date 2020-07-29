
# coding: utf-8


#自由時報

import scrapy
import requests
from bs4 import BeautifulSoup
from lxml import html
from argparse import ArgumentParser
import datetime


parser = ArgumentParser(prog=None, usage=None, description=None, epilog=None)
parser.add_argument("--filter", help="what data you want to search", dest="filter",type=str, default="")


args = parser.parse_args()



###################################
########判斷要不要更新資料#########
###################################

###上一次開始爬的新聞的相關資料
date_last_time = ''
time_last_time = ''
url__last_time  = ''
with open("ltn_news_timestamp.txt") as f:
    tmp = []
    for i in f.readlines():
        tmp.append(i.strip('\n'))
    if len(tmp)>0:
        date_last_time = tmp[0]
        url__last_time = tmp[1]
    else:
        date_last_time = ""
        url__last_time = ""
    #print(date_last_time,time_last_time,url__last_time)



now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d ")
#print(today)

input_url = "http://news.ltn.com.tw/list/breakingnews/all/"
stop = False

links = []
timestamp = []

stop = False
cnt = 0





for i in range(1,30):
    try:
        
        # search each url in each page!!!
        print("page %d"%i)

        #截取自由時報第i頁的資料
        res = BeautifulSoup(requests.get(input_url+str(i)).text)
        

        #用for loop 選取每一欄的資料
        for news in res.select('.list.imm')[0].select('.tit'):
            #print(news)
            
            #取得新聞標題
            title = news.select('p')[0].text
            
            #取得新聞發布時間
            #date = (news.select('a')[0]['href']).split('/')[-3]
            date = news.select('span')[0].text
            if len(date) < 11:
                date = today + date

            #取得URL
            #time = news.select('a')[0].select('time')[0].text
            url = news['href']
            
            
            #print("--------\n")
            print(title)
            #print(date,"    ",len(date))
            #print(url)
            #print("--------\n")

            

            ###判斷要不要從第一頁第一個項目開始爬
            
            if date < date_last_time:
                print("The data is up to date!!!!\nUpdate %d data this time"%cnt)
                stop = True
                break
            elif date == date_last_time and time < time_last_time:
                print("The data is up to date!!!!\nUpdate %d data this time"%cnt)
                stop = True
                break
            elif date == date_last_time and time == time_last_time and url == url__last_time:
                print("The data is up to date!!!!\nUpdate %d data this time"%cnt)
                stop = True
                break

            #爬了多少筆資料的counter
            cnt = cnt + 1


            if args.filter != "":
                if date <= args.filter:
                    stop = True

                    break

            links.append(url)

            print("----------------\nScapying news in")
            print(date)
            print(url)

            ###記錄這次的是從哪一個新聞開始爬起
            if len(timestamp) == 0 : 
                timestamp.append(date)
                timestamp.append(url)

            #這是跑到該網站裡面取標題，如果加這個會慢一些
            #tmp_res = BeautifulSoup(requests.get(tmp).text)
            #print(tmp_res.select('h1')[0].text)
            
        
            
        if stop == True:
            break
    except Exception as e:
        print(e)
    
    last_page_flag = res.select('.p_last')
    if last_page_flag == []:
        break;
    
    
    print("-*-*-*-*-*-*-*-*-*-*--*-**-*--*--*-*-*")
    

#存下這次的url記錄
#包括最新的url 其時間為何，以及有哪些URL等一下要爬
if len(links)>0:

    with open("ltn_news_links.txt",'w') as f:
        for i in links:
            f.write(i)
            f.write('\n')

    with open("ltn_news_timestamp.txt",'w') as f:
        for i in timestamp:
            f.write(i)
            f.write('\n')
    exit(0)
else:
    print('no update!!!')
    exit(1)