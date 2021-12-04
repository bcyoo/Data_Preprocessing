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
                 )
# -










