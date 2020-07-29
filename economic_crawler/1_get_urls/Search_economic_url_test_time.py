
# coding: utf-8

#經濟日報

import scrapy
import requests
from bs4 import BeautifulSoup
from lxml import html
from argparse import ArgumentParser
import datetime

from lxml import etree
import re


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
with open("economic_news_timestamp.txt") as f:
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

#即實新聞網首頁
input_url = "https://money.udn.com/money/breaknews/1001/0/"
stop = False

links = []
timestamp = []

stop = False
cnt = 0


for i in range(1,15):
    try:
        # search each url in each page!!!
        print("page %d"%i)
        res = BeautifulSoup(requests.get(input_url+str(i)).text)

        #根據每一欄的內容，提取新聞資料(新聞發布日期、URL等)
        for news in res.select('.area_body')[0].select('tr')[1:]:

            #time = news.select('a')[0].select('time')[0].text

            #提取新聞標題
            title = news.select('td')[0].select('a')[0].text
            #提取新聞URL
            url = news.select('td')[0].select('a')[0]['href']



            #這邊因為及實新聞的那個頁面(EX "https://money.udn.com/money/breaknews/1001/0/1")並沒有年份資訊
            #所以去他的新聞內文的地方拿年份資訊
            date = etree.HTML(requests.get(url).text).xpath('//*[@id="shareBar"]/div[2]/div/span/text()')[0]

            print(title)
            print(url)
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

            #如果是使用terminal，並且輸入欲爬資料的範圍，並判斷停止條件
            #這邊大部分用預設的即可，除非有想要引用這個函數
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
        
    if len(res.select('.area_body')[0].select('tr')) == 1:
        break;
    
    
    print("-*-*-*-*-*-*-*-*-*-*--*-**-*--*--*-*-*")
    

#存下這次的url記錄
#包括最新的url 其時間為何，以及有哪些URL等一下要爬
if len(links)>0:

    with open("economic_news_links.txt",'w') as f:
        for i in links:
            f.write(i)
            f.write('\n')

    with open("economic_news_timestamp.txt",'w') as f:
        for i in timestamp:
            f.write(i)
            f.write('\n')
    exit(0)
else:
    print('no update!!!')
    exit(1)