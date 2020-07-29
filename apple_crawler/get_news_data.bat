cd C:\Users\tony\Desktop\CHT\progress\20180827~20180831\apple_crawler
call activate
cd 1_get_urls
python Search_apple_url_test_time.py

IF %ERRORLEVEL% == 0 (
cd ../2_Scrapy/apple

::call deactivate
scrapy crawl crawl_content
cd ../..

python 3_load_parse_text.py
call deactivate

@echo off
echo **************************************************
echo **********************finish !!!!*****************
echo **************************************************
echo
@echo on


)
pause
::cmd /k
