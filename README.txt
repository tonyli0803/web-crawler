環境建制

首先環境必須要在Anoconda上執行，因為windows環境下pip install scrapy 會失敗

我使用的環境使使用Anoconda python3的版本

會需要用到的python library包括
pip install scrapy
pip install beautifulsoup4
pip install requests
pip install lxml

然後每一個爬蟲的get_news_data.bat的第一行指令必須修改
EX:
cd C:\Users\tony\Desktop\CHT\progress\20180827~20180831\economic_crawler
必須修改為
cd "你放爬蟲的地方"\"爬蟲的種類_crawler"


程式流程

執行get_news_data.bat

這四個爬蟲的基本流程其實都是差不多的

1. 首先先執行1_get_urls中的Search_udn_url_test_time.py
	主要是要查詢要爬的網址有哪些

	input 爬蟲的種類_news_timestamp.txt
	output 爬蟲的種類_news_timestamp.txt ,爬蟲的種類_news_links.txt

	爬蟲的種類_news_timestamp.txt
	內記錄最後一次爬新聞時，爬到哪一個文章

	如果想抓取2018-08-29 14:12以後的文章
	則將第一行改成"2018-08-29 14:12"即可

2. 再來執行2_Scrapy，使用scrapy crawl crawl_content這個指令執行
	主要的CODE在 2_Scrapy\apple\apple\spiders中的 XXX_news.py
	主要是要下載上一步"查詢要爬的網址"中的新聞稿
	

	input 爬蟲的種類_news_links.txt
	output 今天日期_news.txt


	將下載好的新聞稿存在data資料夾中
	檔名的命名方式以下面為例子
	20180829_news.txt
	就是指20180829到再上一次爬的最後一篇新聞，之間的的所有文章內容

	內部檔案格式如下

	經濟日報、自由時報
	奇數行為該新聞標題，偶數行為新聞內文

	
	聯合報為
	奇數行為該新聞類別(會帶有<<<label>>>)，按照聯合報給的分類方式
	(要聞、選舉、娛樂、運動、全球、社會、專題、產經、房市、健康、生活、文教、評論、地方、兩岸、數位、旅遊、閱讀、雜誌、購物)
	偶數行為新聞內文，新聞內文第一句為新聞標題(會帶有<<<content>>>)

	蘋果日報
	奇數行為該新聞類別(會帶有<<<label>>>)，按照聯合報給的分類方式
	(最新 、焦點、熱門、娛樂時尚、愛播網、社會、國際、政治、生活、火線、3C、吃喝玩樂、體育、財經地產、爆社、論壇、壹週刊)
	偶數行為新聞內文，新聞內文第一句為新聞標題(會帶有<<<content>>>)



3.最後是執行3_load_parse_text.py
	主要提取句子的處理

	input 爬蟲的種類_news_links.txt
	output 今天日期_text