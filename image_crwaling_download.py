# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import os
os.getcwd()

# +
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
import time
import datetime

from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
pd.options.display.max_info_columns =200
pd.options.display.max_columns = 200
pd.options.display.max_info_rows =100
pd.options.display.max_rows = 100

import os
from tqdm import tqdm_notebook
# -

# # 번개장터 이미지크롤링

# ### 주요상품
# - 310	여성의류	w_wear
# - 320	남성의류	m_wear
# - 400	패션액세서리	acc
# - 405	신발	shoes
# - 420	시계_쥬얼리	jewelry
# - 430	가방	bag
# - 600	디지털_가전	electronic
# - 700	스포츠_레저	sports
# - 750	차량_오토바이	car
#
#
# ### 비주류상품
# - 410	뷰티	beauty
# - 500	유아	baby
# - 800	생활_가공식품	living
# - 810	가구_인테리어	interior
# - 900	도서_티켓_문구	book_stationery
# - 910	스타굿즈	stargoods
# - 920	음반_악기	music
# - 930	키덜트	kidult
# - 980	반려동물	pet
# - 990	수집품	collect
# - 999	기타	others

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 드라이버 실행
driver = webdriver.Chrome('C:\\Users\\zezo4\\Desktop\\bunjang\\chromedriver')

# +
# # cat 별 링크 들어가게 세팅
cat_list = [310,320,400,405,420,430,600,700,750]
cat_name = ['w_wear','m_wear','acc','shoes','jewelry','bag','electronic','sports','car']
pages = [1,2,3,4,5]
# 카테고리별 링크 담기
total_df = []

for cat in cat_list:
    # category별 dataframe 생성
    cat_df=pd.DataFrame()
    link=[]    
    for page in pages:
        url = f'https://m.bunjang.co.kr/categories/{cat}?page={page}&req_ref=popular_category'
        driver.get(url)
#         time.sleep(2)
    
        # 페이지마다 사진 100장씩
        for i in range(1,101):
            try:
                ## 페이지만 넘어가서 사진 다운로드.
                link.append(driver.find_element_by_xpath(f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[1]/img').get_attribute('src'))
            except: pass ## 100개 이하일 경우 try except
        print(f'{cat_name[cat_list.index(cat)]}항목 {page}페이지 완료')
        
    cat_df['link'] = link
    cat_df['category'] = cat_name[cat_list.index(cat)]
    ##DF 여러개 일경우 total list를 만들어서 진행
    total_df.append(cat_df)
    print(f'{cat_name[cat_list.index(cat)]}항목 작업 완료\n')
    
print('전체작업 완료')
# -

# 각 작업 파일 저장
# [0]번 부터 저장하게 설정.
for i in range(len(cat_list)):
    total_df[0].to_csv(f'C:\\Users\\zezo4\\Desktop\\bunjang\\data\\image\\image_df\\{cat_name[0]}.csv',index=False)
    total_df[i].to_csv(f'C:\\Users\\zezo4\\Desktop\\bunjang\\data\\image\\image_df\\{cat_name[i]}.csv',index=False)



# # 번개장터 크롤링 이미지 저장

# 파일 불러오기
cat_name = ['w_wear','m_wear','acc','shoes','jewelry','bag','electronic','sports','car']
total_df=[]
for cat in cat_name:
    temp = pd.read_csv(f'C:\\Users\\zezo4\\Desktop\\bunjang\\data\\image\\image_df\\{cat}.csv')
    total_df.append(temp)

# +
from PIL import Image

for cat in range(len(total_df)):
    for i in tqdm_notebook(range(len(total_df[cat])),desc="Image download"):
        url = total_df[cat]['link'].iloc[i]
        os.system("curl " + url + f" > C:\\Users\\zezo4\\Desktop\\bunjang\\data\\image\\{cat_name[cat]}\\c_{i}.jpg")
# -




