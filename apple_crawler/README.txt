按下get_news_data.bat即可開始爬資料
要先設一下get_news_data.bat的第一個指令
cd C:\Users\tony\Desktop\CHT\progress\20180820~20180824\apple_crawler
改成cd "你放這個apple crawler 的檔案路徑"\apple_crawler


get_news_data.bat中
而以下batch指令
call activate python27
call deactivate
是因為我灌python3 anocodo，裡面建python27 (python 2的環境)

因為window 底下灌不了scrapy 才這樣做的




如果使用者在linux環境底下使用
要依照以下順序編寫shell檔

python Search_apple_url_test_time.py  
scrapy crawl crawl_apple_content      
python load_parse_text.py             

即可執行


data 資料夾裡面放的是爬下來的新聞稿
奇數行為新聞標題
偶數行為新聞內文


text 資料夾裡面放的是
把爬下來的新聞稿變成一行一行的句子

