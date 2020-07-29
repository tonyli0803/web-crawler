# -*- coding: utf-8 -*-


from argparse import ArgumentParser
import time
from time import gmtime, strftime
#strftime("%Y%m%d", gmtime()

parser = ArgumentParser(description=" input an xlsx file and output  utf-8 format text")
parser.add_argument("--source_file", help="input the input file path", dest="path", default = "./data/" + strftime("%Y%m%d", gmtime())+"_news.txt",type=str)
parser.add_argument( "--output_file", help="input the output file path", dest="path_out", default = "./text/"+ strftime("%Y%m%d", gmtime())+"_text",type=str)
args = parser.parse_args()


content = []
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
#print(re.split(r"[^\d]","1234hkl1h3k12h34kllkl1341jj"))
#print(re.search(r"^[\u4e00-\u9fa5]+$","的话留在本站否则跳转移动站"))
#簡體字在window cmd 會因為CMD的編碼問題而出現錯誤


ans = []
for i in content:
	#print("\n\n---")
	if type(i)== type(str()):
		#print(i,"----",len(i))
#		print(re.search(r"[\d]+", "vvvva112ddf"))
#		print(re.search(r"^.+$",i))
#		note http://blog.978.tw/2012/05/regular-expression-u4e00-u9fa5-x3130.html
		x = re.search(r"^[\u4e00-\u9fa5A-Za-z\d]+$",i)
		#這似乎只適用繁體中文

		if x == None or x=="" :
			#print("-----------candidate j ----------------\n")
			x = re.split(r"[^\u4e00-\u9fa5A-Za-z\d]+",i)
			if '' in x:
				x.remove("")
				x = filter(lambda a: a != "", x)
			for j in x:
				if re.search(r"^\s$",j) == None and len(j)>4:     #除去所有   "全部都是空白字"    "字數部大於4" 的元素
					ans.append(j)
#					print("j: ",j==" "," -----",len(j),"-----",j)
		else:
			ans.append(i)
#			print("i:  ",i)
#		os.system("pause")

#for i in ans:
#	print(i)


#################################
###########output file###########
#################################
import codecs

with open(args.path_out,'w',encoding='UTF-8') as f:
	counter = 0
	for i in ans:
		counter = counter + 1
		#index = "ABCDEFG%05d "%(counter)
		#f.write(index)

		if i =='\n':
			print('')
		elif i[-1]=='\n':
			f.write(i)
		elif i[0] =='\n':
			tmp = (i[1:]+"\n")
			f.write(tmp)
		elif i=='':
			pass
		elif i == 'label' or i == 'content':
			pass
		else:
			tmp = (i+"\n")
			f.write(tmp)