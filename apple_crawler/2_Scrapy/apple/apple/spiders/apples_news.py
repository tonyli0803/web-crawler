# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from apple.items import AppleItem
import io
from tqdm import tqdm
import time
from time import gmtime, strftime


class AppleCrawler(scrapy.Spider):
	name = 'crawl_content'
	start_urls =['https://tw.finance.appledaily.com/realtime/20180820/1414242/'] #起始抓取連結

	#第一個會先執行的這個函數
	def parse(self, response):
		domain = 'https://tw.appledaily.com/realtimenews/section/new'
		res = BeautifulSoup(response.body)

		urls = []

		#讀取要爬的新聞稿
		with open("../../1_get_urls/apple_news_links.txt") as f:
 
			cnt = 0
			for x in f.readlines():
				urls.append(x.split('\n')[0]) 

		#寫入新聞稿
		for i in tqdm(urls):
			yield scrapy.Request( i,self.parse_detail)

	def parse_detail(self, response):
		res = BeautifulSoup(response.body)

		print("\n\n************this is what we get************\n\n")

		#寫入抓取的內文
		with open("../../data/"+ strftime("%Y%m%d", gmtime()) +"_news.txt","a",encoding='UTF-8') as f :


			#抓取新聞的類別
			news_label = res.select('a.current')[1].text 
			f.write(u'<<<label>>>')
			f.write(news_label)
			f.write(u'\n')


			f.write(u'<<<content>>>')

			#抓取新聞的標題
			f.write(res.select('h1')[0].text)
			f.write(u'。')

			#寫入新聞內文
			for i in res.select('p'):
				f.write(i.text)
			f.write(u'\n')





