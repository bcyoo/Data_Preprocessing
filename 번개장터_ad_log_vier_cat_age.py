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

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
## 이걸 세팅해주세요. 
plt.style.use(['dark_background'])
import chart_studio.plotly as py
import cufflinks as cf
cf.go_offline(connected=True)
import plotly.graph_objects as go

# %run lib.py

pd.options.display.max_info_columns =200
pd.options.display.max_columns = 200
pd.options.display.max_info_rows =999
pd.options.display.max_rows = 999

## csv 파일 불러오기
ad_log_viewer_cat_age_df = pd.read_csv('ad_log_viewer_cat_age.csv')
dataset_df = pd.read_csv('dataset.csv')


ad_log_viewer_cat_age_df.isnull().sum()

N_click_dataset = ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['click'] == 0]
N_click_dataset

click_dataset = ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['click'] == 1]
click_dataset

## 광고에 노출된 대분류
click_category_1 = click_dataset.groupby('대분류명').count().sort_values(by = 'age_range',ascending=False)['user_id_x']
click_category_1

## 광고에 노출되지 않은 대분류
N_click_category_1= N_click_dataset.groupby('대분류명').count().sort_values(by = 'age_range',ascending=False)['user_id_x']
N_click_category_1

## 광고에 노출된 상품 아이디
click_category_1.iplot(kind='bar', theme='white', title='광고에 노출된 대분류')
## 전자제품이 가장 많고 그다음 골프.운동 여성의류 중고차 장신구 남성의류 가방 순

## 광고에 노출된 상품 아이디 Top10
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=click_category_1[:10].index, values=click_category_1[:10].values))
fig.update_layout({
        "title": {"text": "광고에 노출된 대분류 Top10",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()

## 광고에 노출되지 않은 상품 아이디
N_click_category_1.iplot(kind='bar', theme='white', title='광고에 노출되지 않은 대분류')


fig = go.Figure()
fig.add_trace(
    go.Pie(labels=N_click_category_1[:10].index, values=N_click_category_1[:10].values))
fig.update_layout({
        "title": {"text": "광고에 노출되지 않는 대분류 Top10",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()
#대분류 content_id top10 비율 시각화

# ## 광고 노출 상품아이디
#     - 전자제품 > 골프,운동 > 여성의류 > 중고차 > 장신구 > 남성의류 > 가방
#
# ## 광고 노출 X 상품아이디
#     - 전자제품 > 여성의류 > 남성의류 > 가방 > 골프,운동 > 장신구 > 중고차
#     
# - 광고에 노출되는 카테고리는 같으나 비율은 서로 다르다.































## 전자제품
electron_content_id=ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['대분류명']=='전자제품']
electron_content_id

## 노출된 연령 별 전자제품 
electron_age_range=electron_content_id.groupby('age_range')['content_id'].count()
electron_age_range

# 노출된 연령 별 전자제품 
electron_age_range.iplot(kind='bar', theme='white', title='Impression Age Range Electron')

# +
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=electron_age_range.index, values=electron_age_range.values))
fig.update_layout({
        "title": {"text": "Impression Age Range Electron",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()

# 노출된 연령 별 전자제품 
# -

electron_gender=electron_content_id.groupby('gender')['content_id'].count()
electron_gender

# +
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=electron_gender.index, values=electron_gender.values))
fig.update_layout({
        "title": {"text": "Impression Age Range Electron",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()

# 성별 노출 전자제품 
# -

## 전자제품 별 거래수 top10
electron_content_id_pay_top10=electron_content_id.groupby('content_id')['pay_count'].count().sort_values(ascending=False)[:10]
electron_content_id_pay_top10

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=electron_content_id_pay_top10.index, values=electron_content_id_pay_top10.values))
fig.update_layout({
        "title": {"text": "Electron condten_id pay top10",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()
## 전자제품 별 거래수 top10

## 여성의류 
W_category_content_id=ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['대분류명']=='여성의류']
W_category_content_id

## 노출된 여성의류 연령대
Age_W_category_content_id=W_category_content_id.groupby('age_range')['content_id'].count()
Age_W_category_content_id

## 노출된 여성의류 연령대
Age_W_category_content_id.iplot(kind='bar', theme='white', title='Impression Age Range W')

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=Age_W_category_content_id.index, values=Age_W_category_content_id.values))
fig.update_layout({
        "title": {"text": "Impression Age Range W",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()
## 노출된 여성의류 연령대 비율

## 노출된 여성의류 성별
Gen_W_category_content_id=W_category_content_id.groupby('gender')['content_id'].count()
Gen_W_category_content_id
## 1 남자 / 2 여자

import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(
    go.Pie(labels=Gen_W_category_content_id.index, values=Gen_W_category_content_id.values))
fig.update_layout({
        "title": {"text": "Impression Age Range W",
            "font": {"size": 20}},
        "showlegend": True})
fig.show()
## 노출된 여성의류 성별 비율

M_category_content_id=ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['대분류명']=='남성의류']
M_category_content_id





























ad_log_viewer_cat_age_df[ad_log_viewer_cat_age_df['click']==1]

ad_log_viewer_cat_age_df.isnull().sum()

dataset_df[dataset_df['label']==1]


