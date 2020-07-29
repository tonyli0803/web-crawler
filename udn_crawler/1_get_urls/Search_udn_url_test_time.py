
# coding: utf-8

# In[1]:


#-*- coding: utf-8 -*-
#using python3
import sys,requests

from selenium import webdriver
import time, re
from bs4 import BeautifulSoup
from time import sleep


# In[2]:


chrome_path = ".\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
driver = webdriver.Chrome(chrome_path)

driver.implicitly_wait(10)

driver.get('https://udn.com/news/breaknews/1')
sleep(0.1)


# In[3]:


###load上一次開始爬的新聞的相關資料

timestamp = []
date_last_time = ''
url__last_time  = ''
with open("udn_news_timestamp.txt") as f:
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


# In[4]:


'''#第一次 搜索列表
last_html_str=""
start_height = 0
end_height = driver.execute_script("return document.body.scrollHeight")
sleep(0.1)
for i in range(start_height,end_height,200):
#    print('\r   %d'%i)
    sys.stdout.write('\r scrolling to height = '+str(i))
    driver.execute_script('window.scrollTo(0,'+str(i)+')')
    sleep(0.1)
    
html_str = driver.page_source
#這個type 是string,  記錄瀏覽器html5，當前所有內文
    
soup = BeautifulSoup(html_str, "html.parser")
for block in soup.select('.area_body')[1].select('h2 a'):
    print("%s             %70s"%(block.text,block['href']))
    print("\n")
    

'''


# In[ ]:



    


# In[5]:


'''#第二次 搜索列表
#

#不知道為什麼，如果要用以下版本的找按鈕並點擊，如果頁面轉到該按鈕更下方的地方
#就會出現Message: unknown error: Element ... is not clickable at point  的error
#即使使用driver.find_element_by_xpath('//*[@id="more"]/div').click()以及sleep(5)也無效
#但是如果滾輪滾到網頁最上方，再按按鈕，就有效了
driver.execute_script('window.scrollTo(0,0)')
print(driver.find_element_by_link_text("看更多內容"))
driver.find_element_by_link_text("看更多內容").click()


#先睡一下，給他重新算一下參數，不然會拿到舊的scrollHeight
sleep(2)

last_html_str = html_str
start_height = end_height
end_height = driver.execute_script("return document.body.scrollHeight")

for i in range(start_height,end_height,200):
#    print('\r   %d'%i)
    sys.stdout.write('\r scrolling to height = '+str(i))
    driver.execute_script('window.scrollTo(0,'+str(i)+')')
    sleep(0.1)
    
    
#這個type 是string,  記錄瀏覽器html5，當前所有內文
html_str = driver.page_source

print("\nend")

soup1 = BeautifulSoup(last_html_str).select('.area_body')[1].select('h2 a')
soup2 = BeautifulSoup(html_str).select('.area_body')[1].select('h2 a')

print(len(soup1))
print(len(soup2))
#print(soup1==soup2)
print("update %d news" %(len(soup2)-len(soup1)))

for i in range(len(soup1),len(soup2)):
    print(soup2[i])
    print('\n')

sleep(1)'''


# In[6]:


#本格是組裝上面兩個格子的結果，來達成更新n次的效果
n = 200
last_html_str=''
html_str=''
end_height = 0
total_update_news_num = 0
the_news_links = []
stop = False




for i in range(n):
    try:
        print("%dth time"%i)

        #找"看更多內容"這個按鈕後，並且按下去
        driver.execute_script('window.scrollTo(0,0)')
        driver.find_element_by_link_text("看更多內容").click()
        #先睡一下，給他重新算一下參數，不然會拿到舊的scrollHeight
        sleep(2)


        last_html_str = html_str
        start_height = end_height
        #滾滾輪到頁面最下方
        end_height = driver.execute_script("return document.body.scrollHeight")
        sleep(2)
        '''
        for i in range(start_height,end_height,200):
        #    print('\r   %d'%i)
            sys.stdout.write('\r scrolling to height = '+str(i))
            driver.execute_script('window.scrollTo(0,'+str(i)+')')
            sleep(0.1)
        '''

        #這個type 是string,  記錄瀏覽器html5，當前所有內文
        #之所以會有last_news, 跟current_news是因為，要框選出 按下  "看更多內容" 後，新增的新聞
        html_str = driver.page_source

        print("\nend")
        try:
            last_news = BeautifulSoup(last_html_str).select('.area_body')[1].select('h2 a')
        except:
            last_news = []

        current_news = BeautifulSoup(html_str).select('.area_body')[1].select('h2 a')

        current_news_content = BeautifulSoup(html_str).select('.area_body')[1]


#        print(len(last_news))
#        print(len(current_news))
        #rint(soup1==soup2)
#        print("update %d news in this iteration" %(len(current_news)-len(last_news)))
        



        for i in range(len(last_news),len(current_news)):
            print(i)

            #由於UDN 的即實新聞列表並沒有 年份，但它的新聞稿內部有年份
            #所以我嘗試進去每一個新聞取時間資料，速度會慢一些，但不會因為，跨到下一年而有一些bug
            res = BeautifulSoup(requests.get('https://udn.com' + current_news[i]['href']).text)
            date = res.select('div.story_bady_info_author')[0].select('span')[0].text
            print(date)

            title = current_news[i].text
            print(title)
            
            url = 'https://udn.com' + current_news[i]['href']
            print(url)
            
            print('\n')
            
            
            #這邊是再比較date是不是比date_last_time的時間點來的後面
            #而剛剛好如果date比date_last_time的時間點來的後面，用一般字串比較的結果是相同的
            #而且如果date_last_time是空字串，又剛剛好可以使得   "任意 date" > date_last_time
            #可以做出 "沒有上次的check point，把全部資料都爬過一遍的效果"
            
            if date < date_last_time:
                print("The data is up to date!!!!\nUpdate %d data this time"%total_update_news_num)
                stop = True
                break
            elif date == date_last_time and url == url__last_time:
                print("The data is up to date!!!!\nUpdate %d data this time"%total_update_news_num)
                stop = True
                break
                
            total_update_news_num = total_update_news_num + 1
            
            #這邊寫要存的URL
            the_news_links.append([date,current_news[i].text,url])
            
            
            ###記錄這次的是從哪一個新聞開始爬起
            if len(timestamp) == 0 :
                timestamp.append(date)
                timestamp.append(url)
        
            
        
        if stop == True:
            break
    except Exception as e:
        print(e)
        #traceback.print_exc()
        print("tony log :  I guess the crawler reach the end of news, and the '看更多內容' is disappear!!")
        print("tony log :  check it first, then check the error log")
        stop = True

sleep(1)
print("update %d news totally"% total_update_news_num)

driver.close()


# In[53]:

#如果這次有更新的資料，就寫檔udn_news_links.txt   udn_news_timestamp.txt
#udn_news_links.txt存 url      udn_news_timestamp.txt 存最後更新紀錄
if len(the_news_links)>0:

    with open("udn_news_links.txt",'w') as f:
        for i in the_news_links:
#            f.write(i[0])
#            f.write(i[1])
            f.write(i[2])
            f.write('\n')

    with open("udn_news_timestamp.txt",'w') as f:
        for i in timestamp:
            f.write(i)
            f.write('\n')
    exit(0)
else:
    print("no update on udn_news_links")
    exit(1)

