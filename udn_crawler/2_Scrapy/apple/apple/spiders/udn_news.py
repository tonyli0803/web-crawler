# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from apple.items import AppleItem
import io
from tqdm import tqdm
import time
from time import gmtime, strftime
from lxml import etree
import re

class AppleCrawler(scrapy.Spider):
	name = 'crawl_content'
	start_urls =['https://udn.com/news/breaknews/'] #起始抓取連結

	#第一個會先執行的這個函數
	def parse(self, response):
		domain = 'https://udn.com/news'
		res = BeautifulSoup(response.body)

		urls = []

		#讀取要爬的新聞稿
		with open("../../1_get_urls/udn_news_links.txt") as f:

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
		with io.open("../../data/"+ strftime("%Y%m%d", gmtime()) +"_news.txt","a",encoding='UTF-8') as f :

			
			selector = etree.HTML(response.body)
			#抓取新聞的類別
			news_class = selector.xpath('//*[@id="nav"]/a[2]/text()')
			f.write('<<<label>>>')
			f.write(news_class[0])
			f.write(u'\n')
			
			
			f.write('<<<content>>>')

			#寫入新聞的標題
			f.write(res.select('h1')[0].text)
			f.write('。')

			#寫入新聞內文
			for i in res.select('p'):

				try:
					#這邊是說把HTML 有以下的情況時，就不寫入
					#<p>  <script>  ...</script></p>
					#避免把javascript code也寫入新聞中
					if i.select('script') == []:
						f.write(i.text)
					else:
						pass
				except:
					pass
				finally:
					pass
			f.write(u'\n')
