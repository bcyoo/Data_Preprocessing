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

# +
import pathlib
import random
from functools import reduce
from collections import defaultdict

import pandas as pd
import geopandas as gpd # 설치가 조금 힘듭니다. 어려우시면 https://blog.naver.com/PostView.nhn?blogId=kokoyou7620&logNo=222175705733 참고하시기 바랍니다.
import folium
import shapely 
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
import sklearn.cluster
import tensorflow as tf  # 설치 따로 필요합니다. https://chancoding.tistory.com/5 참고 하시면 편해요.

#from geoband import API         이건 설치 필요 없습니다.

import pydeck as pdk                  # 설치 따로 필요합니다.
import os

import pandas as pd


import cufflinks as cf                 # 설치 따로 필요합니다.   
cf.go_offline(connected=True)
cf.set_config_file(theme='polar')

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
plt.rcParams["font.family"] = 'Nanum Gothic'

import numpy as np
from shapely.geometry import Polygon, Point
from numpy import random

import geojson                       # 밑에 Line 84에 추가하여야 하지만 바로 import 안되서 설치 필요

#최적화 solver
import time
from mip import Model, xsum, maximize, BINARY  # 설치 따로 필요합니다.

# +
import sys
'geopandas' in sys.modules

import os
path = os.getcwd()
path

# +
#Pydeck 사용을 위한 함수 정의
import geopandas as gpd 
import shapely 
# Shapely 형태의 데이터를 받아 내부 좌표들을 List안에 반환합니다. 
def line_string_to_coordinates(line_string): 
    if isinstance(line_string, shapely.geometry.linestring.LineString): 
        lon, lat = line_string.xy 
        return [[x, y] for x, y in zip(lon, lat)] 
    elif isinstance(line_string, shapely.geometry.multilinestring.MultiLineString): 
        ret = [] 
        for i in range(len(line_string)): 
            lon, lat = line_string[i].xy 
            for x, y in zip(lon, lat): 
                ret.append([x, y])
        return ret 

def multipolygon_to_coordinates(x): 
    lon, lat = x[0].exterior.xy 
    return [[x, y] for x, y in zip(lon, lat)] 

def polygon_to_coordinates(x): 
    lon, lat = x.exterior.xy 
    return [[x, y] for x, y in zip(lon, lat)] 


# +
##  EDA
#          인구현황 분석
# 목적 : 격자 별 인구 현황을 확인
# 분석데이터 종류
# >> 격자별 인구현황
## 초록색일 경우 인구가 많음, 
## 검은색일 수록 인구가 적음,
## 색이 칠해지지 않은 곳은 값이 0
## 인구 현황 데이터는 현재 100x100 grid로 나누어져 있음
## 추후 데이터 분석을 위해  grid 중심(central point)에 
## 해당하는 point 값을 계산해주고 각각 고유한 grid id를 부여함
## >> 인구 현황을 100x100 point로 설명 할수 있는 결과를 도출하였다.
# -

df_12 = pd.read_csv('속초-고성_2017-20년_혼잡빈도,시간_강도_평균값.csv', encoding = 'utf - 8')
df_12

df_08 = gpd.read_file('08.속초-고성_격자별인구현황.json') # geojson > json
df_08


# +
df_08['val'] = df_08['val'].fillna(0)  
## df_08['val'] NaN값 0으로 채움

df_08['정규화인구'] = df_08['val'] / df_08['val'].max()
## df_8['정규화인구'] 컬럼을 생성하고 val값 / val값 max 계산해서 채움

df_08.head()
# -

df_08['coordinates']=df_08['geometry'].apply(polygon_to_coordinates)
## pydeck을 위한 geometry 좌표를 polygon_to_coordinates함수를
## 통해 coordinates 컬럼을 생성해서 리스트로 넣어줌

# +
## 100x100 grid에서 central point 찾기 
## multipolygon일 경우 cent = 코드[[i[0].centroid.coordsp[0][0], i[0]centroid.coords[0][1]]]
## polygon일 경우 cent = 코드[[i.centroid.coords[0][0], i.centroid.coords[0][1]]]

df_08_list = []
df_08_list2 = []

for i in df_08['geometry']:
    cent = [[i.centroid.coords[0][0], i.centroid.coords[0][1]]]
    df_08_list.append(cent)
    df_08_list2.append(Point(cent[0]))
df_08['coord_cent'] = 0 
df_08['geo_cent'] = 0
df_08['coord_cent'] = pd.DataFrame(df_08_list)
## pydeck을 위한 coordinate type
df_08['geo_cent'] = df_08_list2 
## geopandas를 위한 geometry type

## 쉬운 분석을 위한 임의의 grid id 부여
df_08['grid_id'] = 0
idx = []
for i in range(len(df_08)):
    idx.append(str(i).zfill(5))  ## 5자리 숫자  임의 grid_id 부여
df_08['gird_id'] = pd.DataFrame(idx)

## 인구 현황이 가장 높은 위치

df_08.iloc[df_08['val'].sort_values(ascending=False).index].reindex().head()



# +
## Make Layer
## 사람이 있는 grid만 추출

layer = pdk.Layer( 'PolygonLayer' , ## 사용하는 Layer type
                  df_08[(df_08['val'].isnull()==False) & df_08['val']!=0], # 시각화 DataFrame
                  get_polygon = 'coordinates', #geometry정보가 있는 컬럼 이름
                  get_fill_color = '[900, 255*정규화인구, 0, 정규화인구*10000]', #각 data 별 rgb 또는 rgba 값 (0~255) 
                  pickable = True, # 지도와 interactive 한 동작 on
                  auto_highlight= True # 마우스 오버(hover)시 박스 출력
                 )

# Set the viewport location
center = [128.5918, 38.20701] ## 속초 center lon, lat
view_state = pdk.ViewState(
    longitude = center[0], ## 경도
    latitude = center[1],  ## 위도
    zoom=11
)

# Render 
r = pdk.Deck(layers=[layer], initial_view_state=view_state)

r.to_html()

# +
## 혼잡빈도강도, 혼잡시간강도 분석
# 목적 : 혼잡빈도강도와 혼잡시간빈도를 분석 차량이 많은 위치 파악
## df_10 상세도로망 데이터
## df_12 평일_전일_혼잡빈도강도
## df_13 평일_전일_혼잡빈도강도

## 도로폭이 넓을수록 노란색
## 도로폭이 좁을수록 붉은색
## 선이 굵으면 혼잡 강도가 높음
## 선이 얇으면 혼잡 강도가 낮음


# -

df_10 = gpd.read_file('MOCT_LINK.json')
df_10

df_12 = pd.read_csv("속초-고성_2017-20년_혼잡빈도,시간_강도_평균값.csv", encoding='utf-8')
df_12.head()

df_12.columns

isin_=df_10['ROAD_NAME'].isin(['동해대로', '청학로', '번영로', '중앙로', '장안로', '설악금강대교로', '미시령로', '청대로',
       '온천로', '관광로', '수복로', '중앙시장로', '교동로', '청초호반로', '엑스포로', '조양로', '법대로',
       '설악산로', '동해고속도로(삼척속초)', '장재터마을길', '진부령로', '간성로', '수성로'])
df_10 = df_10.loc[isin_]
df_10

df = df_10
df['coordinates'] = df['geometry'].apply(line_string_to_coordinates)
## df_10의 geometry 컬럼에서 line_string_to_coordinates함수를 사용하여
## coordinates컬럼에 lon경도, lat위도를 리스트로 변환하여 넣어줌
df


df = pd.DataFrame(df) # geopanadas 가 아닌 pandas 의 데이터프레임으로 꼭 바꿔줘야 합니다. 
df.head()

## lanes 컬럼의 차선 비율을 이용하여 WIDTH 컬럼을 생성함
df.loc[df['LANES'] == 1, 'WIDTH'] = '2'
df.loc[df['LANES'] == 2, 'WIDTH'] = '3'
df.loc[df['LANES'] == 3, 'WIDTH'] = '4'
df.loc[df['LANES'] == 4, 'WIDTH'] = '4'
df.loc[df['LANES'] == 5, 'WIDTH'] = '5'
df.loc[df['LANES'] == 6, 'WIDTH'] = '5'
df.loc[df['LANES'] == 7, 'WIDTH'] = '5'

## WIDTH 최대값에서 WIDTH 값을 나누어 정규화도로폭 컬럼을 생성함
df['정규화도로폭'] = df['WIDTH'].apply(int) / df['WIDTH'].apply(int).max()
df

# +
# 혼합빈도강도 양방향 총 합
df_10_ = []

for i in df.LINK_ID:
    df_10_.append([i,sum(df_12[df_12['ITS LINK ID'].apply(str).str.contains(i)].혼잡빈도강도)])
    
df_10_ = pd.DataFrame(df_10_).fillna(0)
df_10_.columns = ["LINK_ID", "혼잡빈도강도합"]
df_10_12 = pd.merge(df, df_10_, on = 'LINK_ID' )

# 혼잡빈도강도 합이 가장 높은 도로
df_10_12.iloc[df_10_12["혼잡빈도강도합"].sort_values(ascending=False).index].reindex().head()

# +
## 도로폭이 넓을수록 노란색
## 도로폭이 좁을수록 붉은색
## 선이 굵으면 혼잡 강도가 높음
## 선이 얇으면 혼잡 강도가 낮음

layer = pdk.Layer('PathLayer', #사용하는 Layer type
                  df_10_12,    # 시각화 DataFrame
                  get_path = 'coordinates', # geometry 정보가 들어있는 컬럼
                  get_width = '혼잡빈도강도합/10', ## 선의 굵기 표시
                  get_color = '[255, 255 * 정규화도로폭, 120]', #각 data 별 rgb 또는 rgba 값 (0~255)
                  pickable = True, # 지도와 interative 한 동작 om
                  auto_highlight = True # 마우스 오버(hover) 시 박스 출력
                )

center = [128.5918, 38.20701] ## 속초 center lon경도, lat위도
view_state = pdk.ViewState(
    longitude = center[0], # 경도
    latitude = center[1], #위도
    zoom = 11
)

#Render

r = pdk.Deck(layers = [layer], initial_view_state = view_state)

r.to_html()


# +
## 혼잡시간강도 양방향 총 합

df_10_ = []

for i in df.LINK_ID:
    df_10_.append([i, sum(df_12[df_12['ITS LINK ID'].apply(str).str.contains(i)].혼잡시간강도)])
    
df_10_ = pd.DataFrame(df_10_).fillna(0)
df_10_.columns = ['LINK_ID', '혼잡시간강도합']
df_10_13 = pd.merge(df, df_10_, on = 'LINK_ID')

##혼잡시간강도합이 가장 높은 도로
df_10_13.iloc[df_10_13['혼잡시간강도합'].sort_values(ascending = False).index].reindex().head()




# +
# df_10_13.loc[df_10_13['혼잡시간강도합'] == 0, '혼잡시간강도합'] = '1'

# +
layer = pdk.Layer( 'PathLayer',
                  df_10_13,
                  get_path = 'coordinates',
                  get_width = '혼잡시간강도합/10',
                  get_color = '[255, 255* 정규화도로폭, 120]',
                  pickable = True,
                  auto_highlight = True
                 )

center = [128.5918, 38.20701]  ## 속초 center lon경도, lat위도
view_state = pdk.ViewState(
    longitude = center[0],
    latitude = center[1],
    zoom=12
)

r = pdk.Deck(layers = [layer], initial_view_state = view_state)

r.to_html()

# +
## 급속충전소 설치가능 장소 필터링
## 목적 : 급속 충전소의 경우 사유지는 제외 해야하므로 설치 가능 장소 필터링이 필요함
## 데이터 : 소유지정보.csv
## 사유지를 포함한 임야, 염전, 도로, 철도 용지, 제방, 하천과 같이 설치가 부적절한 곳을 
## 필터링한 polygon 을 시각화함
## 앞서 도출한 인구현황 100x100 point  데이터셋에서 설치가능한 장소에 해당하는 point를 추출하였음
# -

df_14 = gpd.read_file('14.소유지정보.geojson')
df_14

df_14.columns

len(df_14)

df_14.isna().sum() ## 결측치 확인

# +
df_14_ = df_14[df_14['소유구분코드'].isin(['02','04'])] ## 소유지구분코드 : 국유지 시/군

df_14_possibel = df_14_possible = df_14[df_14['소유구분코드'].isin(['02','04'])
                                        & (df_14['지목코드'].isin(['05','07','14','15','16','17',
                                                              '18','19','20','27'])==False)]
                    ## 02,04 국유지,시/군 포함 나머지 지목코드 임야, 염전, 도로, 철도 용지, 제방 , 하천, 수도시설 제외
    
## geometry to coordinates 
df_14_possible['coordinates'] = df_14_possible['geometry'].apply(polygon_to_coordinates)

## 설치 가능한 모든 polygone을 multipolygon으로 묶음
from shapely.ops import cascaded_union
boundary = gpd.GeoSeries(cascaded_union(df_14_possible['geometry'].buffer(0.001)))

from geojson import Feature, FeatureCollection, dump
MULTIPOLYGON =boundary[0]

features = []
features.append(Feature(geometry=MULTIPOLYGON, properties={"col": "privat"}))
feature_collection = FeatureCollection(features)
with open('geo_possible.geojson', 'w') as f:
    dump(feature_collection, f)

geo_possible= gpd.read_file("geo_possible.geojson")

# +
## 브로드캐스팅을 이용한 요소합 >> layer 평행이동
## 요소합 진행 후, 마지막 데이터를 list로 형변환

v = np.array([-0.0022, 0.0027])
for i in range(len(df_14_possible['coordinates'])):
    for j in range(len(df_14_possible['coordinates'].iloc[i])):
            df_14_possible['coordinates'].iloc[i][j] = list(df_14_possible['coordinates'].iloc[i][j] + v)
    
df_14_possible['coordinates']

# +
layer = pdk.Layer( 'PolygonLayer', # 사용할 Layer 타입 
                  df_14_possible, # 시각화에 쓰일 데이터프레임
                  #df_result_fin[df_result_fin['val']!=0],
                  get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름 
                  get_fill_color='[0, 255*1, 0,140]', # 각 데이터 별 rgb 또는 rgba 값 (0~255) 
                  pickable=True, # 지도와 interactive 한 동작 on 
                  auto_highlight=True # 마우스 오버(hover) 시 박스 출력 
                 ) 

# Set the viewport location 
center = [128.5918, 38.20701] # 속초 센터 [128.5918, 38.20701]
view_state = pdk.ViewState( 
    longitude=center[0], 
    latitude=center[1], 
    zoom=10
) 


# Render 
r = pdk.Deck(layers=[layer], initial_view_state=view_state,
            ) 

    
r.to_html()

# +
## 입지선정지수 개발
## 지역특성 요소 추출
## 100 x 100 point 중 설치 가능한 point 필터링
## > 100x100 중 설치가능한 multipolygon(polygon)에 있는 point를 필터링하는 시간이 굉장히 오래소요됨(약1시간)
## df_result로 최종 분석 할 데이터셋을 만듬.


###### 최종 분석 데이터 정제하기

## 개발 가능한 grid point  찾기
shapely.speedups.enable()
df_result = df_08[['grid_id', 'val', 'geometry', 'coordinates', 'coord_cent', 'geo_cent']]
df_result['val'] = df_result['val'].fillna(0)

## 오래걸림
point_cent = gpd.GeoDataFrame(df_result[['grid_id', 'geo_cent']], geometry = 'geo_cent')
within_points = point_cent.buffer(0.00000001).within(geo_possible.loc[0, 'geometry'])
pd.DataFrame(within_points).to_csv('within_points.csv', index = False)

within_points = pd.read_csv('within_points.csv')
df_result['개발가능'] = 0
df_result['개발가능'][within_point['0']==True] = 1
df_result[df_result['개발가능']==1]
# -


