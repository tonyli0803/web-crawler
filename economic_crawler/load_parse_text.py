# -*- coding: utf-8 -*-


from argparse import ArgumentParser
import time
from time import gmtime, strftime

#這邊雖然有設計可以決定要輸入的文檔，跟輸出的檔名
#不過batch的部分都設計好了，如果只是要自動爬取檔案的話，都用default值就OK了

parser = ArgumentParser(description=" input an xlsx file and output  utf-8 format text")
parser.add_argument("--source_file", help="input the input file path", dest="path", default = "./data/" + strftime("%Y%m%d", gmtime())+"_news.txt",type=str)
parser.add_argument( "--output_file", help="input the output file path", dest="path_out", default = "./text/"+ strftime("%Y%m%d", gmtime())+"_text",type=str)
args = parser.parse_args()


content = []

#讀取新聞稿
with open(args.path,'r',encoding='UTF-8') as f:

	for i in f.readlines():
		content.append(i)
		#print(i)


####################################
###########revise    file###########
####################################
print("\n\n\n\n\nstart using regular expression to find the illegal format\n\n")
import re
import os

#簡體字在window cmd 會因為CMD的編碼問題而出現錯誤，盡量不要出現簡體字

#利用regular expression來 剪取句子
ans = []
for i in content:
	#print("\n\n---")
	if type(i)== type(str()):

#		note http://blog.978.tw/2012/05/regular-expression-u4e00-u9fa5-x3130.html
		x = re.search(r"^[\u4e00-\u9fa5A-Za-z\d]+$",i)
		#這似乎只適用繁體中文

		if x == None or x=="" :

			#利用非"中文字、英文字、空白鍵、數字" 來分段
			#通常有很高的機率選中標點符號
			x = re.split(r"[^\u4e00-\u9fa5A-Za-z\d]+",i)
			if '' in x:
				x.remove("")
				x = filter(lambda a: a != "", x)
			for j in x:
				#除去所有   "全部都是空白字"    "字數不大於4" 的元素
				#這樣的設計是因為，字數小的時候，通常是遺個單詞的機率較高，像是"蔡英文"這樣很不句子
				if re.search(r"^\s$",j) == None and len(j)>4:     #除去所有   "全部都是空白字"    "字數部大於4" 的元素
					ans.append(j)
		else:
			ans.append(i)

#################################
###########output file###########
#################################
import codecs

#寫入裝句子的文檔
with open(args.path_out,'w',encoding='UTF-8') as f:
	counter = 0
	for i in ans:
		counter = counter + 1


		#以下if判斷式是為了讓輸出要式一行一句
		#避免有一行式空的,EX:
		#line 1 : 今天星期三
		#line 2 :
		#line 3 : 我又寫了一個爬蟲
		if i =='\n':
			print('')
		elif i[-1]=='\n':
			f.write(i)
		elif i[0] =='\n':
			tmp = (i[1:]+"\n")
			f.write(tmp)
		elif i=='':
			pass
		#如果是聯合報或著蘋果，由於會加上兩個label用的tag     <<<label>>> 跟 <<<content>>>
		#而在"利用regular expression來 剪取句子"的部分，會把<<<   跟  >>>  給刪除
		#所以這邊還需再刪label 跟 content
		elif i == 'label' or i == 'content':
			pass
		else:
			tmp = (i+"\n")
			f.write(tmp)
		
