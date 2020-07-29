# -*- coding: utf-8 -*-


import scrapy
import requests
from bs4 import BeautifulSoup
from lxml import html
from argparse import ArgumentParser



parser = ArgumentParser(prog=None, usage=None, description=None, epilog=None)
parser.add_argument("--filter", help="what data you want to search", dest="filter",type=str, default="")


args = parser.parse_args()



input_url = "https://tw.appledaily.com/new/realtime/"


#res = BeautifulSoup(requests.get(input_url).text)


links = []
timestamp = []

#print(res.select("nav.page_switch.lisw.fillup")[0].select('a')[1])
#for i in res.select("nav.page_switch.lisw.fillup")[0].select('a'):
#	next_page_url = "https://tw.appledaily.com/new/realtime/"+i['href']
#	print(next_page_url)
	

###################################
########判斷要不要更新資料#########
###################################

###上一次開始爬的新聞的相關資料
date_last_time = ''
time_last_time = ''
url__last_time  = ''
with open("apple_news_timestamp.txt") as f:
	tmp = []
	for i in f.readlines():
		tmp.append(i.strip('\n'))
	if len(tmp)>0:
		date_last_time = tmp[1].split('/')[-3]
		time_last_time = tmp[0]
		url__last_time = tmp[1]
	else:
		date_last_time = ""
		time_last_time = ""
		url__last_time = ""
	#print(date_last_time,time_last_time,url__last_time)





stop = False
cnt = 0
for i in range(60):
	try:
		i=i+1
		# search each url in each page!!!
		print("page %d"%i)
		res = BeautifulSoup(requests.get(input_url+str(i)).text)

		for news in res.select('.rtddt'):
			date = (news.select('a')[0]['href']).split('/')[-3]
			

			time = news.select('a')[0].select('time')[0].text
			url = news.select('a')[0]['href']


			###判斷要不要從第一頁第一個項目開始爬
			
			#print( time,time_last_time,  time > time_last_time ,date == date_last_time and time_last_time < time)


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
			print(date+"  "+time)
			print(url)

			###記錄這次的是從哪一個新聞開始爬起
			if len(timestamp) == 0 : 
				 timestamp.append(time)
				 timestamp.append(url)

			#這是跑到該網站裡面取標題，如果加這個會慢一些
			#tmp_res = BeautifulSoup(requests.get(tmp).text)
			#print(tmp_res.select('h1')[0].text)

			
		if stop == True:
			break
	except:
		traceback.print_exc()
		print(e)
		print("tony log:: maybe reach the end of pages of the website")



if len(links)>0:

	with open("apple_news_links.txt",'w') as f:
		for i in links:
			f.write(i)
			f.write('\n')

	with open("apple_news_timestamp.txt",'w') as f:
		for i in timestamp:
			f.write(i)
			f.write('\n')
	exit(0)
else:
	exit(1)

