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
# E - commerce 상품 추천 Overniew

# +
## 기본적인 사용자흐름

## 개인화추천
## 인기 상품추천
## 성별/연령 기반 추천

# +
#                   홈        >         검색 - 검색어추천

# +
# -연관 대체 상품 추천        상세

# +
# -연관 보완 상품 추천    장바구니 > 구매

# +
## 추천 시스템 분류
# 어떤 요건에 맞춰 어떤 데이터를 활용하여 어떤 모델을 이용하여 어떤 방식으로 계량?

## 요건

# best
# related 관련된
# presonalized 개인화



## 데이터
# Implicit : 어떤 상품을 클릭했는지 검색 햇는지 로그를 갖고 추천


## 모델
# CF 


## 계량방식

# Tok-K Rec.

# +
## E - commerce 특성
# Target Item : product
# Price, brand, Category
# Recency
# Seasonality : Cold - start by Every Season
# Implicit Feedback
# Top-K Recommendation

# +
##  추천 알고리즘 선택

# hybrid Approach
# - e-commerce의 경우 대체적으로 cf를 사용하지만, Content_based 방법도 결합하여 사용

# Collaboratibe Filtering : 주로 item-based CF를 더 많이 사용
# - User-based CF는 적용하기 어려움 : 아이템 수 보다 사용자 수가 더 많아 대규모 계산 필요
#                                   신규로 추가되는 상품이 많음.

# 사용자 메타정보 (세대, Gender) 및 상품 정보 (카테고리, 브랜드, 가격 등)를 활용

# 결합규칙
# - 정적 결합 : 사전에 정해진 weight 사용
# - 동적 결합 : 사용자 프로파일, 아이템 특성에 따라 다른 weight 사용

# +
## Displat 정책

# 1개 아이템 추천
# - 디자인이 수월하고, 모바일 디바이스에도 쉽게 적용
# - 사용자가 원하는 아이템을 찾기까지 탐색이 많이 필요
# - 추천 정확도에 신뢰도가 직접 영향 받음

# K개 아이템 추천
# - 사용자가 원하는 아이템이 포함될 확률이 높아짐
# - 정렬 순서에 대한 신뢰도가 중요함
# - Carousel UI 활용 : 두번째 페이지의 경우 , 첫 페이지 노출 아이템 대비 15 %정보의 클릭

# 설명과 함께 아이템 추천
# - 사용자의 추천 시스템에 대한 신뢰도 상승
# - 구현이 어려움
# - 설명이 정확도보다 더 큰 요소로 작용

# +
# Case Study

## 홈추천
# 방문 매장 기반 메뉴 추천
# 구매 이력 기반 메뉴 추천
# 방문 특정 시점에따른 시점/온도 기반 메뉴 추천

# 메뉴 상세 페이지 대체 상품 추천
# 하단 노출

# 미판매 및 품절 시 대체 상품 추천


# +
## Case Study : 추천 로직

# 동일한 로직으로 생성한 데이터를 여러 영역에서 사용

# 홈 추천
# - 추천 영역에 따라 별도의 상품 정렬 기준 사용
# - eg)  최근 구매 목록 : 사용자별 최근 구매 목록의 재정렬 / 정렬기준 : wx최근 + wx빈도

# 연관 추천
# - 카테고리 제한 없이 유사한 상품 연결

# 대체제 추천
# - 동일 카테고리(음료-음료, 푸드-푸드) 내에서의 유사한 상품 연결

# 보완재 추천
# - 다른 카테고리간의 유사한 상품 연결

# +
# 구매 데이터 기반으로 추천 알고리즘 생성
# SQL로 작성
# 추천 알고리즘을 실행하기 위해 기존 운영 데이터베이스의 테이블을 종합하여 변환하는 작업 중요


# 구매 기록 > 상품, 매장등 각종 로그 및 메타 데이터 추출 > 추천 알고리즘에 적합한 형태로 데이터 가공
# > 연관 추천 결과 생성 > 개인별 최근 구매 목록 생성 > Best 생성 > 최종 결과 생성
# -

# # Data Loading
#
# Load commerce data and show them.
#
# ## Database Initialization

# 확장 기능 로드

## 주피터 노트북에서 SQL을 실행 하는 라이브러리 
# %reload_ext sql
# %run lib.py

# 데이터베이스 접속

# %sql postgresql+psycopg2://postgres:@127.0.0.1:5432/fcrec

# ## Load e-Commerce Data
#
# ### Download data
# Download commerce.zip, then un-zip all files, move it to [FILE_DIRECTORY].
#
# * sampled_events.csv
# * sampled_products.csv
# * sampled_users.csv

# ### Create Tables

# + language="sql"
# drop table if exists cmc_event;
#
# create table cmc_event (
#     session_id 				varchar(40) null,
# 	event_timestamp 		timestamp null,
# 	event_name 				varchar(20) null,
# 	user_no 				varchar(30) null,
# 	item_no 				varchar(30) null,
# 	device_type 			varchar(20) null,
# 	mobile_brand_name 		varchar(50) null,
# 	mobile_model_name 		varchar(50) null,
# 	mobile_marketing_name 	varchar(50) null,
# 	operating_system_version varchar(50) null,
# 	country 				varchar(50) null,
# 	region 					varchar(50) null,
# 	platform 				varchar(10) null
# );
#
# drop table if exists cmc_product;
#
# create table cmc_product (
# 	item_no 				varchar(30) null,
# 	item_name 				varchar(200) null,
# 	image_name				varchar(100) null,
# 	price		 			varchar(20) null,
# 	category1_code 			varchar(20) null,
# 	category1_name 			varchar(20) null,
# 	category2_code 			varchar(20) null,
# 	category2_name 			varchar(20) null,
# 	category3_code 			varchar(20) null,
# 	category3_name 			varchar(20) null,
# 	brand_no 				varchar(20) null,
# 	brand_name 				varchar(100) null
# );
#
#
# drop table if exists cmc_user;
#
# create table cmc_user (
# 	user_no 				varchar(30) null,
# 	birth_date 				varchar(20) null,
# 	gender 					varchar(10) null
# );
# -

# ### Copy Data from File to Table

# Set file paths

# +
FILE_DIRECTORY = 'C:\\fcrec\\'

event_file = FILE_DIRECTORY + 'sampled_events.csv'
product_file = FILE_DIRECTORY + 'sampled_products.csv'
user_file = FILE_DIRECTORY + 'sampled_users.csv'
# -

# Load files

# + language="sql"
#
# copy cmc_event from :event_file delimiter ',' csv header;
#
# copy cmc_product from :product_file delimiter ',' csv header;
#
# copy cmc_user from :user_file delimiter ',' csv header;
# -

# ## Check Data

# Check event data

# %sql select * from cmc_event limit 10;

# Check user data

# %sql select * from cmc_user limit 10;

# Check product data

# %sql select * from cmc_product limit 10;

# Read data into variable

# result = %sql select item_no, item_name, image_name, price, category1_name, category2_name, category3_name, brand_name from cmc_product limit 10;

result

# Or use _ to store last results

result = _
result

# ### Use executeQuery() function to get results

# +
query = '''
    select item_no, item_name, image_name, price, category1_name, category2_name, category3_name, brand_name 
    from cmc_product 
    limit 10;
'''

result = executeQuery(query)
result
# -

result

# ### Display item images

displayItemInRows(result)


