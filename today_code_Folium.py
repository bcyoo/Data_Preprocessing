# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# 한글폰트 사용
import platform
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    f_path = '/Library/Fonts/Arial Unicode.ttf'
elif platform.system() == 'Windows':
    f_path = 'c:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=f_path).get_name()
rc('font', family=font_name)

print('Hangul font is set!')
# -

plt.style.use('default')

import pandas as pd
import numpy as np
from plotnine import * # 데이터 시각화 
import re # 정규표현식
# 지도 표현
import folium

df = pd.read_csv('./전국도시공원정보표준데이터.csv', encoding = 'cp949')
df.shape

df.head()

df.info()

df.isnull().sum() # sum()을 통해 결측치 확인가능

# +
import missingno as msno # 결측치 시각화

msno.matrix(df)
# -

df.columns # df의 columns명을 출력함

df.drop(columns=['공원보유시설(운동시설)', '공원보유시설(유희시설)', '공원보유시설(편익시설)', '공원보유시설(교양시설)',
       '공원보유시설(기타시설)'], inplace=True)

df.shape

# +
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


font_path = r'C:\Users\zezo4\NanumBarunGothic.ttf'
fontprop = fm.FontProperties(fname=font_path, size=18)

# +
## 위경도 시각화 
## 지도를 출력해 보니 특정 지역만 있다.
## 결측치인 nan 데이터 때문에 다른 데이터가 제대로 보이지 않음.
## nan 데이터를 제거 하고 다시 그려본다.

(ggplot(df)  ## gg plot 으로 시각화
 + aes(x='경도', y='위도')
 + geom_point() # 점포인트로 찍음
 + theme(text=element_text(family='NaumBarunGothic'))
) 

# +
## 데이터 전처리
# -

df.dtypes

# df['공원면적'] = df['공원면적'].str.replace(',', '').astype(float) #dtype가 object일 경우 str 필요함
df['공원면적'] = df['공원면적'].replace(',', '').astype(float)
df['공원면적'].head()

## 공원면적비율은 데이터를 시각화할 때 공원이 크면 큰점, 작으면 작은점으로 지도상이나 산점도에서 표현하기 위해 sqrt루트를 씌우고 크기를 0.01로 조정함
df['공원면적비율'] = df['공원면적'].apply(lambda x : np.sqrt(x) * 0.01 )
df['공원면적비율'].head()

df['소재지도로명주소'].isnull().sum() # 소재지도로명주소 결측치

df['소재지지번주소'].isnull().sum() # 소재지지번주소 결측치

## 도로명 주소가 null 이고 소재지지번 주소가 있다면 이 소재지지번 주소로 채워준다
df.loc[(df['소재지도로명주소'].isnull()) & (df['소재지지번주소'].notnull())].shape

## 도로명 주소를 지번주소로 채워주는 함수.
df['소재지도로명주소'].fillna(df['소재지지번주소'], inplace=True)

df['소재지도로명주소'].isnull().sum()

# 도로명 주소 중에 null 값을 지번주소 notnull 값으로 채움해서 다시 한번 확인했더니 도로명주소가 업식에 shape 0이 나옴
df_loc = df.loc[(df['소재지도로명주소'].isnull()) & (df['소재지지번주소'].notnull())]
df_loc.shape

## 소재지도로명 주소로 시도와 구군으로 나누려고하는데, 
## 소재지도로명 주소가 공백으로 구분되어있어서 
## str.split(' ',expand=True)[0]를 통해 0번째는 맨 처음에 나오는 시도 컬럼을 만들어서 도로명 주소 앞에 것만 채워줌
df['시도'] = df['소재지도로명주소'].str.split(' ', expand=True)[0]
df.head(3)

## 소재지도로명주소로 시도와 구군을 나누려고한다. 소재지도로명 컬럼 안에 주소가 공백으로 나누어져 있기 때문에
## df['소재지도로명주소'].str.split(' ', expand=True)[1]를 통해 2번째인 구군을 df['구군에'] 넣는 함수이다.
df['구군'] = df['소재지도로명주소'].str.split(' ', expand=True)[1]
df.head(3)

## 
df.describe()

df[['위도', '경도']].describe()

(ggplot(df)  ## gg plot 으로 시각화
 + aes(x='경도', y='위도')
 + geom_point() # 점포인트로 찍음
 + theme(text=element_text(family=font_name))
) 

# +
# 위 지도의 위도와 경도의 아웃라이어 데이터를 제외하고 출력해보자
# 좀 더 정확하게 출력하려면 대한민국 위경도 데이터 범위를 다시 넣어줍니다.


## 위도가 32보다 크거나, 경도가 132보다 낮은것에 대해서 
df_loc_notnull = df.loc[(df['위도'] > 32) & (df['경도'] < 132) & df['시도'].notnull()]
df_loc_notnull.shape
# -

# 위경도가 잘못 입력된 데이터를 봅니다.
# 주소가 잘못되지는 않았습니다.
# 주소를 통해 위경도를 다시 받아올ㅇ 필요가 있습니다.
df.loc[(df['위도'] < 26) | (df['경도'] >= 132)]

df_loc_notnull['시도'].value_counts()
