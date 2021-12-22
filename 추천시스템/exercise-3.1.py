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
# FILE_DIRECTORY = 'C:\\fcrec\\'

# event_file = FILE_DIRECTORY + 'sampled_events.csv'
# product_file = FILE_DIRECTORY + 'sampled_products.csv'
# user_file = FILE_DIRECTORY + 'sampled_users.csv'
# -

# Load files

# +
# # %%sql

# # copy cmc_event from :event_file delimiter ',' csv header;

# # copy cmc_product from :product_file delimiter ',' csv header;

# # copy cmc_user from :user_file delimiter ',' csv header;

# + language="sql"
#
# \copy cmc_event
# from 'C:\Users\zezo4\Desktop\SSAC_강의자료\패스트캠퍼스_추천시스템\workshop\02commerce\data\sampled_events.csv'
# delimiter ',' csv header;
#
# \copy cmc_product
# from 'C:\Users\zezo4\Desktop\SSAC_강의자료\패스트캠퍼스_추천시스템\workshop\02commerce\data\sampled_products.csv'
# delimiter ',' csv header;
#
# \copy cmc_user
# from 'C:\Users\zezo4\Desktop\SSAC_강의자료\패스트캠퍼스_추천시스템\workshop\02commerce\data\sampled_users.csv'
# delimiter ',' csv header;
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


