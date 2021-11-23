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
 + theme(text=element_text(family='font_name'))
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

(ggplot(df_loc_notnull)
 + aes(x='경도', y='위도', color='시도')
 + geom_point()
 + theme(text=element_text(family=font_name))
)

# 전국적으로 어린이 공원이 가장 많은 것으로 보입니다.
# 제주도는 한라산 아래 해안선과 유사한 모습으로 공원이 배치되어 있는 모습이 인상적입니다.
(ggplot(df_loc_notnull)
 + aes(x='경도', y='위도', color='공원구분', size='공원면적비율')
 + geom_point()
 + theme(text=element_text(family=font_name))
)

# 어린이 공원을 제외하고 찍어보자
# 다음으로 많은 근린공원과 소공원이 많이 보임.
(ggplot(df_loc_notnull.loc[df_loc_notnull['공원구분'] != '어린이공원'])
 + aes(x='경도', y='위도', color='공원구분', size='공원면적비율')
 + geom_point()
 + theme(text=element_text(family=font_name))
)

df_loc_notnull.head()

# +
## 시도별 공원 비율

df_do = pd.DataFrame(df['시도'].value_counts())
df_do_normalize = pd.DataFrame(df['시도'].value_counts(normalize=True))
df_sido = df_do.merge(df_do_normalize, left_index=True, right_index=True).reset_index()
df_sido.columns = ['시도', '합계', '비율']
df_sido.sort_values(by=['합계'], ascending=False)
df_sido
# -

# 경기도가 압도적으로 많음
(ggplot(df_sido.sort_values(by=['합계'], ascending=False))
 + aes(x='시도', y='합계')
 + geom_bar(stat='identity', position='dodge', fill='green')
 + coord_flip()
 + theme(text=element_text(family=font_name))
)

df_type = df['공원구분'].value_counts().reset_index()
df_type.columns = ('공원구분', '합계')
df_type

#공원구분별 합계
(ggplot(df_type)
 + aes(x='공원구분', y='합계')
 + geom_bar(stat='identity', position='dodge', fill='green')
 + coord_flip()
 + theme(text=element_text(family=font_name))
)


# +
## 경기도에 가장 많은 공원이 있습니다.
## 어떻게 분포 하였는지 확인해보자

gg = df.loc[df['시도'] == '경기도']
gg.shape
# -

gg_df = gg['공원구분'].value_counts().reset_index()
gg_df.columns = ('공원구분', '합계')
gg_df

(ggplot(gg)
 + aes(x='경도', y='위도', color='공원구분', size='공원면적비율') 
 + geom_point()
 + geom_jitter(color='lightgray', alpha=0.25)
 + theme(text=element_text(family=font_name))
)

gg_suwon = gg.loc[gg['구군'] == '수원시']

(ggplot(gg_suwon)
 + aes(x='경도', y='위도', color='공원구분', size='공원면적비율') 
 + geom_point()
 + geom_jitter(color='lightgray', alpha=0.25)
 + theme(text=element_text(family=font_name))
)

# +
geo_df = gg_suwon
map = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()], zoom_start=13)

for n in geo_df.index:
    df_name = geo_df.loc[n, '공원명'] + '-' + geo_df.loc[n, '소재지도로명주소']
    icon_color = 'blue'
    folium.CircleMarker(
        location=[geo_df.loc[n, '위도'], geo_df.loc[n, '경도']],
        radius=geo_df['공원면적비율'][n],
        popup=park_name,
        color=icon_color,
        fill=True,
        fill_color=icon_color
    ).add_to(map)
    
map


## null값으로 출력 불가능.
# -

# 경기도 일부 공원만 보기
df_type = r'.*((역사|체육|수변|문화|묘지)공원).*'
gg_sample = gg.loc[gg['공원구분'].str.match(df_type)]

gg_sample.shape

(ggplot(gg_sample)
 + aes(x='경도', y='위도', color='공원구분') 
 + geom_point()
 + geom_jitter(fill='green', color='lightgray', alpha=0.25)
 + theme(text=element_text(family=font_name))
)

seoul = df[df['시도'] == '서울특별시']
seoul.shape

seoul.head()

(ggplot(seoul)
 + aes(x='경도', y='위도', color='공원구분') 
 + geom_point()
 + theme(text=element_text(family=font_name))
)

seoul[seoul["경도"] > 127.4]

seoul['공원구분'].value_counts()

seoul_playground = df.loc[(df['공원구분'] == '어린이공원') & (df['시도'] == '서울특별시')]
seoul_playground.head()

(ggplot(seoul)
 + aes(x='경도', y='위도', fill='구군')
 + geom_point()
 + theme(text=element_text(family=font_name))
)

gu = '강남구 강동구 강북구 강서구 관악구 광진구 구로구 금천구 노원구 도봉구 동대문구 동작구 마포구 서대문구 서초구 성동구 성북구 송파구 양천구 영등포구 용산구 은평구 종로구 중구 중랑구'
gu = gu.split(' ')
print('서울에는 {}개의 구가 있다.'.format(len(gu)))

# 무악동이 구군 데이터에 잘못 들어와 있다. 전처리 해줄 필요가 있다.
seoul_gu = seoul['구군'].value_counts().reset_index()
seoul_gu_count = seoul_gu.shape[0]
seoul_gu.head()

seoul_gu.columns = ['구군', '합계']
seoul_gu = seoul_gu.sort_values(by='합계', ascending=False)
# 누락된 구를 찾기 위해 데이터프레임에 들어있는 구군을 추출한다.
seoul_gu_unique = seoul_gu['구군'].unique()
seoul_gu_unique

exclude_gu = [g for g in gu if not g in seoul_gu_unique] 
print('누락된 구: {}'.format(exclude_gu))
error_gu = [g for g in seoul_gu_unique if not g in gu] 
print('잘못들어간 구: {}'.format(error_gu))
# 전체 구에서 누락된 구와 잘못들어간 구를 제외하고 계산해 본다.
seoul_gu_count = len(gu) - len(exclude_gu) - len(error_gu)
print('아래 데이터를 보니 몇개 구가 누락된것을 알 수 있다. 전체 {}개 구 중 {}개 구만 있다.'.format(len(gu), seoul_gu_count))
seoul_gu

# 위 데이터에서는 송파, 서초, 양천, 강남구에 공원이 많은 것으로 보여집니다.
# 강남3구는 공원만 표시해 봅니다.
geo_df = seoul.loc[seoul['구군'].str.match( r'((강남|서초|송파)구)')]
geo_df = geo_df.loc[(geo_df['위도'].notnull()) & (geo_df['경도'].notnull())]
geo_df.isnull().sum()

# 서초구 데이터에 잘못된 위경도 데이터가 보입니다. 
(ggplot(geo_df)
 + aes(x='경도', y='위도', fill='구군', size='공원면적비율')
 + geom_point()
 + theme(text=element_text(family=font_name))
)

geo_df.shape



# +
geo_df.shape
map = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()], zoom_start=13)

for n in geo_df.index:
    park_name = geo_df.loc[n, '공원명'] + ' - ' + geo_df.loc[n, '소재지도로명주소']
    folium.Marker([geo_df.loc[n, '위도'], geo_df.loc[n, '경도']], popup=park_name).add_to(map)
map
